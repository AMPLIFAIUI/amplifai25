#!/usr/bin/env python3
"""
AMPLIFAI SIMPLE MODEL DISSECTION
Quick analysis of all 12 GGUF models to create supermodel blueprint
"""

import os
import json
import time
from pathlib import Path
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def discover_models() -> List[Path]:
    """Find all GGUF models"""
    logger.info("🔍 Discovering GGUF models...")
    
    models_dir = Path("Amplifai/models")
    gguf_files = []
    
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.gguf'):
                model_path = Path(root) / file
                gguf_files.append(model_path)
                logger.info(f"Found: {model_path}")
                
    return gguf_files

def analyze_model(model_path: Path) -> Dict[str, Any]:
    """Analyze a single model"""
    logger.info(f"🔬 Analyzing: {model_path.name}")
    
    try:
        from llama_cpp import Llama
        
        # Load model
        model = Llama(
            model_path=str(model_path),
            n_ctx=256,
            verbose=False,
            n_threads=2
        )
        
        # Test capabilities
        capabilities = {}
        
        # Math test
        start_time = time.time()
        try:
            output = model("2 + 2 =", max_tokens=5, echo=False)
            response = output['choices'][0]['text'] if output.get('choices') else ""
            math_time = time.time() - start_time
            capabilities['math'] = {
                'response': response.strip(),
                'time': math_time,
                'score': 1.0 if '4' in response else 0.5
            }
        except:
            capabilities['math'] = {'score': 0.0, 'time': 1.0}
            
        # Code test
        start_time = time.time()
        try:
            output = model("def hello():", max_tokens=10, echo=False)
            response = output['choices'][0]['text'] if output.get('choices') else ""
            code_time = time.time() - start_time
            capabilities['code'] = {
                'response': response.strip(),
                'time': code_time,
                'score': 1.0 if any(word in response.lower() for word in ['print', 'return', 'pass']) else 0.5
            }
        except:
            capabilities['code'] = {'score': 0.0, 'time': 1.0}
            
        # Reasoning test
        start_time = time.time()
        try:
            output = model("The sky is blue because", max_tokens=15, echo=False)
            response = output['choices'][0]['text'] if output.get('choices') else ""
            reason_time = time.time() - start_time
            capabilities['reasoning'] = {
                'response': response.strip(),
                'time': reason_time,
                'score': 1.0 if len(response.strip()) > 10 else 0.5
            }
        except:
            capabilities['reasoning'] = {'score': 0.0, 'time': 1.0}
            
        # Overall performance
        avg_time = sum(cap.get('time', 1.0) for cap in capabilities.values()) / len(capabilities)
        avg_score = sum(cap.get('score', 0.0) for cap in capabilities.values()) / len(capabilities)
        
        # Determine specialization
        specializations = []
        if 'deepseek' in model_path.name.lower() or 'coder' in model_path.name.lower():
            specializations.append('coding')
        if 'gemma' in model_path.name.lower() or 'reasoning' in model_path.name.lower():
            specializations.append('reasoning')
        if 'qwen' in model_path.name.lower():
            specializations.append('multilingual')
        if 'llama' in model_path.name.lower():
            specializations.append('general')
        if 'mythomax' in model_path.name.lower():
            specializations.append('creative')
        if 'hermes' in model_path.name.lower():
            specializations.append('dialogue')
        if 'phi' in model_path.name.lower():
            specializations.append('compact')
        if 'grok' in model_path.name.lower():
            specializations.append('analytical')
            
        return {
            'name': model_path.stem,
            'path': str(model_path),
            'size_mb': model_path.stat().st_size / (1024 * 1024),
            'capabilities': capabilities,
            'avg_inference_time': avg_time,
            'avg_capability_score': avg_score,
            'specializations': specializations,
            'status': 'analyzed'
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to analyze {model_path}: {e}")
        return {
            'name': model_path.stem,
            'path': str(model_path),
            'size_mb': model_path.stat().st_size / (1024 * 1024),
            'status': 'failed',
            'error': str(e)
        }

def create_supermodel_blueprint(model_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create supermodel blueprint from all analyses"""
    logger.info("🎨 Creating SUPERMODEL blueprint...")
    
    # Filter successful analyses
    successful = [m for m in model_analyses if m.get('status') == 'analyzed']
    
    # Calculate total parameters (rough estimate)
    total_size_mb = sum(m['size_mb'] for m in successful)
    estimated_params = int(total_size_mb * 1_000_000)  # Very rough estimate
    
    # Find best models for each capability
    best_math = max(successful, key=lambda m: m['capabilities'].get('math', {}).get('score', 0))
    best_code = max(successful, key=lambda m: m['capabilities'].get('code', {}).get('score', 0))
    best_reasoning = max(successful, key=lambda m: m['capabilities'].get('reasoning', {}).get('score', 0))
    
    # Group by specialization
    specialization_groups = {}
    for model in successful:
        for spec in model.get('specializations', ['general']):
            if spec not in specialization_groups:
                specialization_groups[spec] = []
            specialization_groups[spec].append(model['name'])
            
    # Create routing strategy
    routing_strategy = {
        'math_queries': best_math['name'],
        'code_queries': best_code['name'],
        'reasoning_queries': best_reasoning['name'],
        'general_queries': 'ensemble_all',
        'creative_queries': 'mythomax' if any('mythomax' in m['name'] for m in successful) else best_reasoning['name'],
        'dialogue_queries': 'hermes' if any('hermes' in m['name'] for m in successful) else best_reasoning['name']
    }
    
    blueprint = {
        'supermodel_info': {
            'name': 'AMPLIFAI_SUPERMODEL_v1',
            'type': 'intelligent_ensemble',
            'component_models': len(successful),
            'total_estimated_parameters': estimated_params,
            'total_size_mb': total_size_mb,
            'creation_timestamp': time.time()
        },
        'component_models': successful,
        'specialization_groups': specialization_groups,
        'routing_strategy': routing_strategy,
        'ensemble_config': {
            'default_strategy': 'best_match',
            'fallback_strategy': 'ensemble_vote',
            'confidence_threshold': 0.7,
            'max_parallel_inferences': 3
        },
        'optimization_profile': {
            'target_inference_time': min(m.get('avg_inference_time', 1.0) for m in successful),
            'target_accuracy': max(m.get('avg_capability_score', 0.5) for m in successful),
            'memory_efficiency': 'dynamic_loading',
            'scaling_strategy': 'adaptive'
        }
    }
    
    return blueprint

def main():
    """Main dissection process"""
    logger.info("🔥 STARTING AMPLIFAI MODEL DISSECTION")
    logger.info("=" * 60)
    
    # Discover models
    model_paths = discover_models()
    
    if not model_paths:
        logger.error("❌ No models found!")
        return
        
    logger.info(f"📊 Found {len(model_paths)} models to analyze")
    
    # Analyze each model
    analyses = []
    for model_path in model_paths:
        analysis = analyze_model(model_path)
        analyses.append(analysis)
        
    # Create supermodel blueprint
    blueprint = create_supermodel_blueprint(analyses)
    
    # Save blueprint
    with open('supermodel_blueprint.json', 'w') as f:
        json.dump(blueprint, f, indent=2)
        
    # Print results
    print("\n🔥 AMPLIFAI MODEL DISSECTION COMPLETE! 🔥")
    print("=" * 60)
    print(f"Models Analyzed: {len([a for a in analyses if a.get('status') == 'analyzed'])}")
    print(f"Total Size: {blueprint['supermodel_info']['total_size_mb']:.1f} MB")
    print(f"Estimated Parameters: {blueprint['supermodel_info']['total_estimated_parameters']:,}")
    print(f"Specializations: {list(blueprint['specialization_groups'].keys())}")
    print("\n🎯 SUPERMODEL BLUEPRINT SAVED!")
    print("=" * 60)
    
    # Show routing strategy
    print("\n🧠 INTELLIGENT ROUTING STRATEGY:")
    for query_type, model in blueprint['routing_strategy'].items():
        print(f"  {query_type}: {model}")
        
    return blueprint

if __name__ == "__main__":
    main()
