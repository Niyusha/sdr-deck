#!/usr/bin/env python3
"""
Minimal API test script that checks FastAPI functionality
without hardware dependencies
"""

import sys
import os
from pathlib import Path

# Add src/api to path
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

def test_basic_imports():
    """Test if basic FastAPI imports work"""
    try:
        from fastapi import FastAPI
        from uvicorn import run
        print("✓ FastAPI and uvicorn imports successful")
        return True
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False

def test_api_structure():
    """Test if the API structure is valid without hardware imports"""
    try:
        # Mock hardware modules that aren't available in WSL
        import types
        
        # Create mock modules
        mock_rpi = types.ModuleType('RPi')
        mock_gpio = types.ModuleType('GPIO')
        mock_rpi.GPIO = mock_gpio
        sys.modules['RPi'] = mock_rpi
        sys.modules['RPi.GPIO'] = mock_gpio
        
        mock_board = types.ModuleType('board')
        sys.modules['board'] = mock_board
        
        mock_adafruit_ina219 = types.ModuleType('adafruit_ina219')
        mock_adafruit_ina219.ADCResolution = object
        mock_adafruit_ina219.BusVoltageRange = object
        mock_adafruit_ina219.INA219 = object
        mock_adafruit_ina219.Mode = object
        mock_adafruit_ina219.Gain = object
        sys.modules['adafruit_ina219'] = mock_adafruit_ina219
        
        # Test main.py structure
        with open('../api/main.py', 'r') as f:
            content = f.read()
            
        # Check for FastAPI setup
        if 'FastAPI(' in content and 'uvicorn' in content:
            print("✓ FastAPI application structure found")
            return True
        else:
            print("✗ FastAPI application structure not found")
            return False
            
    except Exception as e:
        print(f"✗ API structure test failed: {e}")
        return False

def test_config_file():
    """Test if config.ini is readable"""
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('../api/config.ini')
        
        if 'server' in config.sections():
            print("✓ Configuration file is readable")
            print(f"  Server config found: {dict(config['server'])}")
            return True
        else:
            print("✗ Server section not found in config")
            return False
            
    except Exception as e:
        print(f"✗ Config file test failed: {e}")
        return False

def test_basic_fastapi_app():
    """Create a minimal FastAPI app to test functionality"""
    try:
        from fastapi import FastAPI
        
        app = FastAPI(title="SDR Cyberdeck Test")
        
        @app.get("/test")
        def test_endpoint():
            return {"status": "working", "message": "API test successful"}
            
        print("✓ Basic FastAPI app creation successful")
        return True
        
    except Exception as e:
        print(f"✗ FastAPI app creation failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing SDR Cyberdeck API...")
    print("=" * 50)
    
    tests = [
        ("Basic imports", test_basic_imports),
        ("API structure", test_api_structure),
        ("Config file", test_config_file),
        ("FastAPI app", test_basic_fastapi_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API structure looks good.")
        exit(0)
    else:
        print("❌ Some tests failed. Check the issues above.")
        exit(1)