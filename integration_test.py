#!/usr/bin/env python3
"""
AMPLIFAI COMPREHENSIVE INTEGRATION TEST SUITE
Testing all systems: Backend, Liquid UI, Preview Panel, and Autonomous Economy
"""

import asyncio
import json
import logging
import time
import threading
import subprocess
import sys
from pathlib import Path
import requests
import websocket
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.ui_url = "http://localhost:8001"
        self.preview_url = "http://localhost:8002"
        self.economy_url = "http://localhost:8003"
        self.services = {}
        self.test_results = {}
        
    async def start_all_services(self):
        """Start all Amplifai services"""
        services = {
            'backend': {
                'script': 'Amplifai/models/production_backend.py',
                'port': 8000,
                'url': self.base_url
            },
            'liquid_ui': {
                'script': 'Amplifai/webui/liquid_ui_system.py',
                'port': 8001,
                'url': self.ui_url
            },
            'preview_panel': {
                'script': 'Amplifai/webui/amp_preview_panel.py',
                'port': 8002,
                'url': self.preview_url
            },
            'autonomous_economy': {
                'script': 'Amplifai/autonomous_economy.py',
                'port': 8003,
                'url': self.economy_url
            }
        }
        
        logger.info("Starting all Amplifai services...")
        
        for service_name, config in services.items():
            try:
                # Start service in background
                process = subprocess.Popen([
                    sys.executable, config['script']
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                self.services[service_name] = {
                    'process': process,
                    'config': config,
                    'started': time.time()
                }
                
                logger.info(f"Started {service_name} service on port {config['port']}")
                
                # Wait a bit between starts
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to start {service_name}: {e}")
                
        # Wait for all services to initialize
        logger.info("Waiting for services to initialize...")
        await asyncio.sleep(10)
        
    async def test_backend_models(self):
        """Test the production backend model loading and inference"""
        logger.info("Testing backend model systems...")
        
        try:
            # Test health check
            response = requests.get(f"{self.base_url}/")
            assert response.status_code == 200, "Backend health check failed"
            
            # Test model list
            response = requests.get(f"{self.base_url}/models/available")
            models = response.json()
            assert len(models) > 0, "No models available"
            logger.info(f"Found {len(models)} available models")
            
            # Test model inference with multiple models
            test_prompts = [
                "Explain quantum computing",
                "Write a Python function to sort a list",
                "What is the meaning of life?",
                "Create a business plan outline"
            ]
            
            results = []
            for prompt in test_prompts:
                # Ensure models is a list and safely get first 3
                model_list = models if isinstance(models, list) else []
                for model in model_list[:3]:  # Test first 3 models
                    try:
                        # Handle both dict and string model formats
                        model_name = model.get("name") if isinstance(model, dict) else str(model)
                        response = requests.post(f"{self.base_url}/models/infer", json={
                            "model_name": model_name,
                            "prompt": prompt,
                            "max_tokens": 100
                        }, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            results.append({
                                'model': model_name,
                                'prompt': prompt,
                                'response': result.get('response', ''),
                                'time': result.get('inference_time', 0)
                            })
                            logger.info(f"✓ {model_name} inference successful")
                        else:
                            logger.warning(f"✗ {model_name} inference failed: {response.status_code}")
                            
                    except Exception as e:
                        logger.error(f"Error testing {model_name}: {e}")
                        
            self.test_results['backend'] = {
                'models_loaded': len(models),
                'successful_inferences': len(results),
                'average_response_time': sum(r['time'] for r in results) / len(results) if results else 0
            }
            
        except Exception as e:
            logger.error(f"Backend test failed: {e}")
            self.test_results['backend'] = {'error': str(e)}
            
    async def test_liquid_ui(self):
        """Test the liquid UI system"""
        logger.info("Testing Liquid UI system...")
        
        try:
            # Test UI health
            response = requests.get(self.ui_url)
            assert response.status_code == 200, "UI service not responding"
            
            # Test WebSocket connection
            ws_url = self.ui_url.replace('http', 'ws') + '/ws'
            
            # Test UI adaptation
            response = requests.post(f"{self.ui_url}/adapt", json={
                "user_id": "test_user",
                "interaction_type": "chat",
                "context": "testing"
            })
            assert response.status_code == 200, "UI adaptation failed"
            
            # Test Mini AMP avatar
            response = requests.post(f"{self.ui_url}/mini-amp/chat", json={
                "message": "Hello, how are you?",
                "user_id": "test_user"
            })
            assert response.status_code == 200, "Mini AMP chat failed"
            
            avatar_response = response.json()
            assert 'response' in avatar_response, "No avatar response"
            
            # Test performance analytics
            response = requests.get(f"{self.ui_url}/analytics")
            assert response.status_code == 200, "Analytics endpoint failed"
            
            self.test_results['liquid_ui'] = {
                'service_healthy': True,
                'avatar_responding': True,
                'analytics_working': True
            }
            
        except Exception as e:
            logger.error(f"Liquid UI test failed: {e}")
            self.test_results['liquid_ui'] = {'error': str(e)}
            
    async def test_preview_panel(self):
        """Test the AMP preview panel"""
        logger.info("Testing AMP Preview Panel...")
        
        try:
            # Test preview service health
            response = requests.get(self.preview_url)
            assert response.status_code == 200, "Preview service not responding"
            
            # Test code execution
            python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")
"""
            
            response = requests.post(f"{self.preview_url}/execute", json={
                "code": python_code,
                "language": "python"
            })
            assert response.status_code == 200, "Code execution failed"
            
            execution_result = response.json()
            assert execution_result.get('success'), "Code execution not successful"
            
            # Test JavaScript execution
            js_code = """
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

const result = factorial(5);
console.log(`Factorial(5) = ${result}`);
"""
            
            response = requests.post(f"{self.preview_url}/execute", json={
                "code": js_code,
                "language": "javascript"
            })
            assert response.status_code == 200, "JS execution failed"
            
            # Test model comparison
            response = requests.post(f"{self.preview_url}/compare", json={
                "prompt": "Explain machine learning",
                "models": ["deepseek", "qwen"]
            })
            
            if response.status_code == 200:
                comparison = response.json()
                assert 'results' in comparison, "No comparison results"
                
            self.test_results['preview_panel'] = {
                'service_healthy': True,
                'python_execution': True,
                'javascript_execution': True,
                'model_comparison': response.status_code == 200
            }
            
        except Exception as e:
            logger.error(f"Preview panel test failed: {e}")
            self.test_results['preview_panel'] = {'error': str(e)}
            
    async def test_autonomous_economy(self):
        """Test the autonomous economy system"""
        logger.info("Testing Autonomous Economy system...")
        
        try:
            # Test economy service health
            response = requests.get(self.economy_url)
            assert response.status_code == 200, "Economy service not responding"
            
            # Test resource allocation
            response = requests.post(f"{self.economy_url}/allocate", json={
                "task_type": "inference",
                "requirements": {
                    "cpu": 2,
                    "memory": 4,
                    "gpu": 1
                },
                "priority": "high"
            })
            assert response.status_code == 200, "Resource allocation failed"
            
            allocation = response.json()
            assert 'allocation_id' in allocation, "No allocation ID returned"
            
            # Test market operations
            response = requests.get(f"{self.economy_url}/market/status")
            assert response.status_code == 200, "Market status failed"
            
            market_status = response.json()
            assert 'prices' in market_status, "No market prices"
            
            # Test economic agents
            response = requests.get(f"{self.economy_url}/agents")
            assert response.status_code == 200, "Agents endpoint failed"
            
            # Test performance optimization
            response = requests.post(f"{self.economy_url}/optimize", json={
                "target": "cost",
                "constraints": {"max_latency": 1000}
            })
            assert response.status_code == 200, "Optimization failed"
            
            self.test_results['autonomous_economy'] = {
                'service_healthy': True,
                'resource_allocation': True,
                'market_operations': True,
                'optimization': True
            }
            
        except Exception as e:
            logger.error(f"Autonomous economy test failed: {e}")
            self.test_results['autonomous_economy'] = {'error': str(e)}
            
    async def test_integration_flows(self):
        """Test integration between all systems"""
        logger.info("Testing system integration flows...")
        
        try:
            # Test complete workflow: UI -> Backend -> Economy -> Preview
            
            # 1. Start with UI interaction
            ui_response = requests.post(f"{self.ui_url}/mini-amp/chat", json={
                "message": "Generate a Python function and execute it",
                "user_id": "integration_test"
            })
            
            if ui_response.status_code == 200:
                ui_result = ui_response.json()
                
                # 2. Use response to generate code via backend
                backend_response = requests.post(f"{self.base_url}/models/infer", json={
                    "model_name": "deepseek",
                    "prompt": "Write a Python function to calculate prime numbers up to n",
                    "max_tokens": 200
                })
                
                if backend_response.status_code == 200:
                    backend_result = backend_response.json()
                    generated_code = backend_result.get('response', '')
                    
                    # 3. Execute code in preview panel
                    if generated_code:
                        preview_response = requests.post(f"{self.preview_url}/execute", json={
                            "code": generated_code,
                            "language": "python"
                        })
                        
                        # 4. Optimize resources via economy
                        if preview_response.status_code == 200:
                            economy_response = requests.post(f"{self.economy_url}/optimize", json={
                                "target": "performance",
                                "context": "code_execution"
                            })
                            
                            self.test_results['integration'] = {
                                'ui_to_backend': True,
                                'backend_to_preview': True,
                                'preview_to_economy': economy_response.status_code == 200,
                                'full_flow_success': True
                            }
                        else:
                            self.test_results['integration'] = {'error': 'Preview execution failed'}
                    else:
                        self.test_results['integration'] = {'error': 'No code generated'}
                else:
                    self.test_results['integration'] = {'error': 'Backend inference failed'}
            else:
                self.test_results['integration'] = {'error': 'UI interaction failed'}
                
        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            self.test_results['integration'] = {'error': str(e)}
            
    async def test_performance_metrics(self):
        """Test overall system performance"""
        logger.info("Testing performance metrics...")
        
        try:
            start_time = time.time()
            
            # Concurrent load test
            async def load_test():
                tasks = []
                
                # Create multiple concurrent requests
                for i in range(10):
                    tasks.append(asyncio.create_task(self.single_request_test(i)))
                    
                results = await asyncio.gather(*tasks, return_exceptions=True)
                return results
                
            load_results = await load_test()
            
            end_time = time.time()
            total_time = end_time - start_time
            
            successful_requests = len([r for r in load_results if not isinstance(r, Exception)])
            
            self.test_results['performance'] = {
                'total_requests': len(load_results),
                'successful_requests': successful_requests,
                'total_time': total_time,
                'requests_per_second': len(load_results) / total_time,
                'success_rate': successful_requests / len(load_results)
            }
            
        except Exception as e:
            logger.error(f"Performance test failed: {e}")
            self.test_results['performance'] = {'error': str(e)}
            
    async def single_request_test(self, request_id):
        """Single request for load testing"""
        try:
            response = requests.post(f"{self.base_url}/models/infer", json={
                "model_name": "deepseek",
                "prompt": f"Test request {request_id}",
                "max_tokens": 50
            }, timeout=10)
            return response.status_code == 200
        except:
            return False
            
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("Generating test report...")
        
        report = {
            'timestamp': time.time(),
            'test_results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed_tests': len([t for t in self.test_results.values() if not isinstance(t, dict) or 'error' not in t]),
                'failed_tests': len([t for t in self.test_results.values() if isinstance(t, dict) and 'error' in t])
            }
        }
        
        # Save report
        with open('integration_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("AMPLIFAI INTEGRATION TEST REPORT")
        print("="*60)
        
        for test_name, result in self.test_results.items():
            status = "✗ FAILED" if isinstance(result, dict) and 'error' in result else "✓ PASSED"
            print(f"{test_name.upper()}: {status}")
            
            if isinstance(result, dict) and 'error' not in result:
                for key, value in result.items():
                    print(f"  {key}: {value}")
            elif isinstance(result, dict) and 'error' in result:
                print(f"  Error: {result['error']}")
                
        print("\n" + "="*60)
        print(f"SUMMARY: {report['summary']['passed_tests']}/{report['summary']['total_tests']} tests passed")
        print("="*60)
        
        return report
        
    def cleanup(self):
        """Clean up all started services"""
        logger.info("Cleaning up services...")
        
        for service_name, service_info in self.services.items():
            try:
                service_info['process'].terminate()
                logger.info(f"Terminated {service_name} service")
            except:
                pass
                
    async def run_full_test_suite(self):
        """Run the complete integration test suite"""
        logger.info("Starting Amplifai Integration Test Suite...")
        
        try:
            # Start all services
            await self.start_all_services()
            
            # Run all tests
            await self.test_backend_models()
            await self.test_liquid_ui()
            await self.test_preview_panel()
            await self.test_autonomous_economy()
            await self.test_integration_flows()
            await self.test_performance_metrics()
            
            # Generate report
            report = self.generate_report()
            
            return report
            
        except Exception as e:
            logger.error(f"Test suite failed: {e}")
            
        finally:
            self.cleanup()

async def main():
    """Main test runner"""
    tester = IntegrationTester()
    
    try:
        report = await tester.run_full_test_suite()
        
        # Exit with appropriate code
        if report and report['summary']['failed_tests'] == 0:
            print("\n🎉 All tests passed! Amplifai system is working correctly.")
            sys.exit(0)
        else:
            print("\n⚠️  Some tests failed. Check the report for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\nTest suite error: {e}")
        tester.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
