#!/usr/bin/env python3
"""
AMPLIFAI SYSTEM STATUS DASHBOARD
Real-time monitoring and status of all Amplifai components
"""

import asyncio
import json
import time
import requests
import websocket
import threading
from datetime import datetime
import sys

class AmplifaiStatusDashboard:
    def __init__(self):
        self.services = {
            'backend': {
                'name': 'Model Backend',
                'url': 'http://localhost:8000',
                'endpoints': ['/', '/models/available', '/health'],
                'status': 'unknown'
            },
            'liquid_ui': {
                'name': 'Liquid UI System',
                'url': 'http://localhost:8001',
                'endpoints': ['/', '/analytics'],
                'status': 'unknown'
            },
            'preview_panel': {
                'name': 'AMP Preview Panel',
                'url': 'http://localhost:8002',
                'endpoints': ['/', '/status'],
                'status': 'unknown'
            },
            'autonomous_economy': {
                'name': 'Autonomous Economy',
                'url': 'http://localhost:8003',
                'endpoints': ['/', '/market/status'],
                'status': 'unknown'
            }
        }
        
        self.system_stats = {
            'start_time': time.time(),
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'models_loaded': 0,
            'active_connections': 0
        }
        
    def check_service_health(self, service_name, service_config):
        """Check the health of a single service"""
        try:
            # Basic health check
            response = requests.get(service_config['url'], timeout=5)
            if response.status_code == 200:
                service_config['status'] = 'healthy'
                service_config['last_check'] = datetime.now()
                
                # Additional endpoint checks
                endpoint_status = {}
                for endpoint in service_config['endpoints']:
                    try:
                        ep_response = requests.get(service_config['url'] + endpoint, timeout=3)
                        endpoint_status[endpoint] = ep_response.status_code == 200
                    except:
                        endpoint_status[endpoint] = False
                        
                service_config['endpoints_status'] = endpoint_status
                
                # Get specific metrics if available
                if service_name == 'backend':
                    self.get_backend_metrics(service_config)
                elif service_name == 'autonomous_economy':
                    self.get_economy_metrics(service_config)
                    
                return True
            else:
                service_config['status'] = 'unhealthy'
                service_config['error'] = f"HTTP {response.status_code}"
                return False
                
        except Exception as e:
            service_config['status'] = 'unreachable'
            service_config['error'] = str(e)
            return False
            
    def get_backend_metrics(self, service_config):
        """Get specific metrics from the backend service"""
        try:
            response = requests.get(service_config['url'] + '/models/available', timeout=3)
            if response.status_code == 200:
                models = response.json()
                self.system_stats['models_loaded'] = len(models)
                service_config['models'] = models
                
            # Get performance stats if available
            try:
                stats_response = requests.get(service_config['url'] + '/stats', timeout=3)
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    service_config['performance'] = stats
            except:
                pass
                
        except:
            pass
            
    def get_economy_metrics(self, service_config):
        """Get specific metrics from the economy service"""
        try:
            response = requests.get(service_config['url'] + '/market/status', timeout=3)
            if response.status_code == 200:
                market = response.json()
                service_config['market'] = market
                
        except:
            pass
            
    async def monitor_all_services(self):
        """Monitor all services continuously"""
        while True:
            try:
                for service_name, service_config in self.services.items():
                    self.check_service_health(service_name, service_config)
                    
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"Monitor error: {e}")
                await asyncio.sleep(5)
                
    def print_dashboard(self):
        """Print the status dashboard"""
        # Clear screen (works on most terminals)
        print("\033[2J\033[H", end="")
        
        # Header
        print("="*80)
        print("🔥 AMPLIFAI SYSTEM STATUS DASHBOARD 🔥")
        print("="*80)
        
        # System uptime
        uptime = time.time() - self.system_stats['start_time']
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        
        print(f"System Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"Models Loaded: {self.system_stats['models_loaded']}")
        print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Service status
        print("SERVICE STATUS:")
        print("-" * 80)
        
        for service_name, service_config in self.services.items():
            status = service_config.get('status', 'unknown')
            name = service_config['name']
            url = service_config['url']
            
            # Status icon
            if status == 'healthy':
                icon = "🟢"
            elif status == 'unhealthy':
                icon = "🟡"
            elif status == 'unreachable':
                icon = "🔴"
            else:
                icon = "⚪"
                
            print(f"{icon} {name:<20} {status:<12} {url}")
            
            # Show endpoint status
            if 'endpoints_status' in service_config:
                for endpoint, ep_status in service_config['endpoints_status'].items():
                    ep_icon = "✓" if ep_status else "✗"
                    print(f"    {ep_icon} {endpoint}")
                    
            # Show specific metrics
            if service_name == 'backend' and 'models' in service_config:
                models = service_config['models']
                print(f"    Models: {len(models)} loaded")
                
            if service_name == 'autonomous_economy' and 'market' in service_config:
                market = service_config['market']
                if 'active_agents' in market:
                    print(f"    Market: {market.get('active_agents', 0)} agents")
                    
            # Show errors
            if 'error' in service_config:
                print(f"    Error: {service_config['error']}")
                
            print()
            
        # Overall system health
        healthy_services = len([s for s in self.services.values() if s.get('status') == 'healthy'])
        total_services = len(self.services)
        
        print("-" * 80)
        if healthy_services == total_services:
            print("🎉 SYSTEM STATUS: ALL SYSTEMS OPERATIONAL")
        elif healthy_services > 0:
            print(f"⚠️  SYSTEM STATUS: PARTIAL ({healthy_services}/{total_services} services healthy)")
        else:
            print("🚨 SYSTEM STATUS: ALL SERVICES DOWN")
            
        print("="*80)
        
        # Quick access info
        if healthy_services > 0:
            print("QUICK ACCESS:")
            if self.services['liquid_ui']['status'] == 'healthy':
                print("🖥️  Main Interface: http://localhost:8001")
            if self.services['backend']['status'] == 'healthy':
                print("🔌 API Backend: http://localhost:8000")
            if self.services['preview_panel']['status'] == 'healthy':
                print("⚡ Preview Panel: http://localhost:8002")
            if self.services['autonomous_economy']['status'] == 'healthy':
                print("💰 Economy Dashboard: http://localhost:8003")
                
        print("="*80)
        print("Press Ctrl+C to exit")
        
    async def run_dashboard(self):
        """Run the live dashboard"""
        print("Starting Amplifai Status Dashboard...")
        
        # Start monitoring in background
        monitor_task = asyncio.create_task(self.monitor_all_services())
        
        try:
            while True:
                self.print_dashboard()
                await asyncio.sleep(2)  # Update every 2 seconds
                
        except KeyboardInterrupt:
            print("\nShutting down dashboard...")
            monitor_task.cancel()
            
        except Exception as e:
            print(f"Dashboard error: {e}")
            monitor_task.cancel()

def main():
    """Main entry point"""
    dashboard = AmplifaiStatusDashboard()
    
    try:
        asyncio.run(dashboard.run_dashboard())
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Dashboard failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
