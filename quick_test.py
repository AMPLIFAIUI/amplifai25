#!/usr/bin/env python3
"""
SIMPLE AMPLIFAI COMPONENT TEST
Quick test of each component individually
"""

import requests
import time
import subprocess
import sys
import json

def test_backend():
    """Test just the backend"""
    print("🔧 Testing Production Backend...")
    
    try:
        # Start backend
        proc = subprocess.Popen([sys.executable, "Amplifai/models/production_backend.py"])
        
        # Wait for startup
        time.sleep(5)
        
        # Test health
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
              # Test models
            response = requests.get("http://localhost:8000/models", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get('models', [])
                print(f"✅ Found {len(models)} models")
                
                # Test inference if models available
                if models:
                    model_name = models[0].get("name", "amp-coder")
                    response = requests.post("http://localhost:8000/infer", json={
                        "model_name": model_name,
                        "prompt": "Hello, world!",
                        "max_tokens": 20
                    }, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Inference successful: {result.get('response', '')[:50]}...")
                    else:
                        print(f"❌ Inference failed: {response.status_code}")
            else:
                print(f"❌ Models endpoint failed: {response.status_code}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
    finally:
        try:
            proc.terminate()
        except:
            pass

def test_liquid_ui():
    """Test liquid UI"""
    print("\n🎨 Testing Liquid UI...")
    
    try:
        # Start UI
        proc = subprocess.Popen([sys.executable, "Amplifai/webui/liquid_ui_system.py"])
        
        # Wait for startup
        time.sleep(5)
        
        # Test health
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Liquid UI is running!")
            
            # Test Mini AMP
            response = requests.post("http://localhost:8001/mini-amp/chat", json={
                "message": "Hello",
                "user_id": "test"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Mini AMP responding: {result.get('response', '')[:50]}...")
            else:
                print(f"❌ Mini AMP failed: {response.status_code}")
        else:
            print(f"❌ UI health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Liquid UI test failed: {e}")
    finally:
        try:
            proc.terminate()
        except:
            pass

def test_preview_panel():
    """Test preview panel"""
    print("\n⚡ Testing Preview Panel...")
    
    try:
        # Start preview panel
        proc = subprocess.Popen([sys.executable, "Amplifai/webui/amp_preview_panel.py"])
        
        # Wait for startup
        time.sleep(5)
        
        # Test health
        response = requests.get("http://localhost:8002/", timeout=5)
        if response.status_code == 200:
            print("✅ Preview Panel is running!")
            
            # Test code execution
            response = requests.post("http://localhost:8002/execute", json={
                "code": "print('Hello from Amplifai!')",
                "language": "python"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Code execution successful: {result.get('success', False)}")
            else:
                print(f"❌ Code execution failed: {response.status_code}")
        else:
            print(f"❌ Preview Panel health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Preview Panel test failed: {e}")
    finally:
        try:
            proc.terminate()
        except:
            pass

def test_economy():
    """Test autonomous economy"""
    print("\n💰 Testing Autonomous Economy...")
    
    try:
        # Start economy
        proc = subprocess.Popen([sys.executable, "Amplifai/autonomous_economy.py"])
        
        # Wait for startup
        time.sleep(5)
        
        # Test health
        response = requests.get("http://localhost:8003/", timeout=5)
        if response.status_code == 200:
            print("✅ Autonomous Economy is running!")
            
            # Test market status
            response = requests.get("http://localhost:8003/market/status", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Market operational with {result.get('active_agents', 0)} agents")
            else:
                print(f"❌ Market status failed: {response.status_code}")
        else:
            print(f"❌ Economy health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Economy test failed: {e}")
    finally:
        try:
            proc.terminate()
        except:
            pass

def main():
    print("🚀 AMPLIFAI COMPONENT TESTING")
    print("=" * 50)
    
    # Test each component
    test_backend()
    test_liquid_ui()
    test_preview_panel()
    test_economy()
    
    print("\n" + "=" * 50)
    print("🎯 Component testing complete!")

if __name__ == "__main__":
    main()
