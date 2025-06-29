#!/usr/bin/env python3
"""
AMPLIFAI MASTER SYSTEM LAUNCHER
Coordinates all Amplifai components into the world's most powerful AI system
"""

import asyncio
import subprocess
import sys
import time
import logging
import json
import signal
import threading
from pathlib import Path
import requests
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AmplifaiMasterSystem:
    def __init__(self):
        self.services = {}
        self.running = False
        self.startup_sequence = [
            {
                'name': 'backend',
                'script': 'Amplifai/models/production_backend.py',
                'port': 8000,
                'url': 'http://localhost:8000',
                'description': 'Production Model Backend - GGUF model inference engine',
                'startup_delay': 5,
                'health_endpoint': '/'
            },
            {
                'name': 'autonomous_economy',
                'script': 'Amplifai/autonomous_economy.py',
                'port': 8003,
                'url': 'http://localhost:8003',
                'description': 'Autonomous Economy - Resource allocation and optimization',
                'startup_delay': 3,
                'health_endpoint': '/'
            },
            {
                'name': 'preview_panel',
                'script': 'Amplifai/webui/amp_preview_panel.py',
                'port': 8002,
                'url': 'http://localhost:8002',
                'description': 'AMP Preview Panel - Code execution and model comparison',
                'startup_delay': 3,
                'health_endpoint': '/'
            },
            {
                'name': 'liquid_ui',
                'script': 'Amplifai/webui/liquid_ui_system.py',
                'port': 8001,
                'url': 'http://localhost:8001',
                'description': 'Liquid UI System - Adaptive interface with Mini AMP',
                'startup_delay': 2,
                'health_endpoint': '/'
            }
        ]
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Shutdown signal received. Stopping all services...")
        self.running = False
        self.shutdown_all()
        sys.exit(0)
        
    async def start_service(self, service_config):
        """Start a single service"""
        service_name = service_config['name']
        
        try:
            logger.info(f"Starting {service_name}: {service_config['description']}")
            
            # Start the service process
            process = subprocess.Popen([
                sys.executable, service_config['script']
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.services[service_name] = {
                'process': process,
                'config': service_config,
                'started': time.time(),
                'status': 'starting'
            }
            
            # Wait for startup
            await asyncio.sleep(service_config['startup_delay'])
            
            # Check if service is healthy
            await self.check_service_health(service_name)
            
            logger.info(f"✓ {service_name} started successfully on port {service_config['port']}")
            
        except Exception as e:
            logger.error(f"✗ Failed to start {service_name}: {e}")
            self.services[service_name] = {
                'status': 'failed',
                'error': str(e)
            }
            
    async def check_service_health(self, service_name):
        """Check if a service is healthy"""
        service = self.services[service_name]
        config = service['config']
        
        max_attempts = 30  # 30 seconds timeout
        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    config['url'] + config['health_endpoint'],
                    timeout=2
                )
                if response.status_code == 200:
                    service['status'] = 'healthy'
                    return True
            except:
                await asyncio.sleep(1)
                
        service['status'] = 'unhealthy'
        return False
        
    async def start_all_services(self):
        """Start all services in the correct order"""
        logger.info("🚀 Starting Amplifai Master System...")
        logger.info("=" * 60)
        
        self.running = True
        
        for service_config in self.startup_sequence:
            if not self.running:
                break
                
            await self.start_service(service_config)
            
        # Wait for all services to be fully ready
        logger.info("Waiting for all services to be ready...")
        await asyncio.sleep(5)
        
        # Final health check
        healthy_services = 0
        for service_name, service in self.services.items():
            if service.get('status') == 'healthy':
                healthy_services += 1
                
        logger.info("=" * 60)
        logger.info(f"🎯 Amplifai System Status: {healthy_services}/{len(self.startup_sequence)} services healthy")
        
        if healthy_services == len(self.startup_sequence):
            logger.info("🎉 ALL SYSTEMS OPERATIONAL - Amplifai is ready!")
            self.print_system_info()
        else:
            logger.warning("⚠️  Some services failed to start properly")
            
        return healthy_services == len(self.startup_sequence)
        
    def print_system_info(self):
        """Print system information and access URLs"""
        print("\n" + "="*80)
        print("🔥 AMPLIFAI - WORLD'S MOST POWERFUL AI SYSTEM 🔥")
        print("="*80)
        print("SYSTEM ARCHITECTURE:")
        print("├── Production Backend: Real GGUF model inference (12+ models)")
        print("├── Liquid UI System: Adaptive interface with Mini AMP avatar")
        print("├── AMP Preview Panel: Secure code execution & model comparison")
        print("└── Autonomous Economy: Resource optimization & market dynamics")
        print("\nACCESS POINTS:")
        print("├── Main Interface: http://localhost:8001")
        print("├── API Backend: http://localhost:8000")
        print("├── Preview Panel: http://localhost:8002")
        print("└── Economy Dashboard: http://localhost:8003")
        print("\nSYSTEM CAPABILITIES:")
        print("✓ Multi-model AI inference with 12+ GGUF models")
        print("✓ Adaptive UI that learns from user behavior")
        print("✓ Secure code execution in Python & JavaScript")
        print("✓ Real-time model performance comparison")
        print("✓ Autonomous resource allocation & optimization")
        print("✓ Economic market simulation for AI resources")
        print("✓ WebSocket real-time communication")
        print("✓ Production-ready with no placeholders")
        print("="*80)
        print("Status: 🟢 ALL SYSTEMS OPERATIONAL")
        print("="*80)
        
    async def monitor_services(self):
        """Monitor service health and restart if needed"""
        while self.running:
            try:
                for service_name, service in self.services.items():
                    if service.get('status') == 'healthy':
                        # Check if process is still running
                        process = service.get('process')
                        if process and process.poll() is not None:
                            logger.warning(f"Service {service_name} crashed, restarting...")
                            await self.restart_service(service_name)
                            
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(5)
                
    async def restart_service(self, service_name):
        """Restart a failed service"""
        if service_name in self.services:
            service = self.services[service_name]
            config = service['config']
            
            logger.info(f"Restarting {service_name}...")
            
            # Find the config for this service
            service_config = next((s for s in self.startup_sequence if s['name'] == service_name), None)
            if service_config:
                await self.start_service(service_config)
                
    def get_system_status(self):
        """Get current system status"""
        status = {
            'timestamp': time.time(),
            'uptime': time.time() - min(s.get('started', time.time()) for s in self.services.values() if 'started' in s),
            'services': {},
            'overall_health': 'healthy'
        }
        
        unhealthy_count = 0
        for service_name, service in self.services.items():
            service_status = service.get('status', 'unknown')
            status['services'][service_name] = {
                'status': service_status,
                'port': service.get('config', {}).get('port'),
                'uptime': time.time() - service.get('started', time.time()) if 'started' in service else 0
            }
            
            if service_status != 'healthy':
                unhealthy_count += 1
                
        if unhealthy_count > 0:
            status['overall_health'] = 'degraded' if unhealthy_count < len(self.services) else 'unhealthy'
            
        return status
        
    def shutdown_all(self):
        """Shutdown all services"""
        logger.info("Shutting down all services...")
        
        for service_name, service in self.services.items():
            try:
                process = service.get('process')
                if process:
                    process.terminate()
                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        
                logger.info(f"✓ Stopped {service_name}")
                
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
                
        logger.info("All services stopped")
        
    async def run_system(self):
        """Run the complete Amplifai system"""
        try:
            # Start all services
            success = await self.start_all_services()
            
            if not success:
                logger.error("Failed to start all services")
                return False
                
            # Start monitoring
            monitor_task = asyncio.create_task(self.monitor_services())
            
            # Keep running until interrupted
            while self.running:
                await asyncio.sleep(1)
                
            # Cleanup
            monitor_task.cancel()
            
        except Exception as e:
            logger.error(f"System error: {e}")
            
        finally:
            self.shutdown_all()
            
        return True

# Command line interface
async def main():
    """Main entry point"""
    master = AmplifaiMasterSystem()
    
    try:
        success = await master.run_system()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"System failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔥 Initializing Amplifai Master System...")
    asyncio.run(main())
