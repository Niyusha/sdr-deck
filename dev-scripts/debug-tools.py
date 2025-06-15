#!/usr/bin/env python3
"""
Remote debugging tools for SDR Cyberdeck development
Provides utilities for debugging the API remotely
"""

import requests
import json
import argparse
import time
import sys
from typing import Dict, Any, Optional

class SDRDebugger:
    """Debug tools for SDR Cyberdeck API"""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.timeout = 10
    
    def ping(self) -> bool:
        """Check if the API server is responding"""
        try:
            response = self.session.put(f"{self.base_url}/ping")
            if response.status_code == 200:
                data = response.json()
                return data.get("success", False) and data.get("response") == "pong"
            return False
        except Exception as e:
            print(f"❌ Ping failed: {e}")
            return False
    
    def get_systems(self) -> Optional[Dict[str, Any]]:
        """Get all configured systems"""
        try:
            response = self.session.get(f"{self.base_url}/systems")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get systems: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting systems: {e}")
            return None
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """Get system status"""
        try:
            response = self.session.get(f"{self.base_url}/status")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get status: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting status: {e}")
            return None
    
    def get_config(self) -> Optional[Dict[str, Any]]:
        """Get system configuration"""
        try:
            response = self.session.get(f"{self.base_url}/config")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get config: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting config: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        print("🔍 Running health check...")
        
        results = {
            "ping": False,
            "systems": False,
            "status": False,
            "config": False,
            "errors": []
        }
        
        # Test ping
        print("  📡 Testing ping...")
        results["ping"] = self.ping()
        if results["ping"]:
            print("    ✅ Ping successful")
        else:
            print("    ❌ Ping failed")
            results["errors"].append("API server not responding to ping")
        
        # Test systems endpoint
        print("  🏗️ Testing systems endpoint...")
        systems = self.get_systems()
        if systems:
            results["systems"] = True
            print(f"    ✅ Found {len(systems)} systems")
        else:
            print("    ❌ Systems endpoint failed")
            results["errors"].append("Cannot retrieve systems list")
        
        # Test status endpoint
        print("  📊 Testing status endpoint...")
        status = self.get_status()
        if status:
            results["status"] = True
            print("    ✅ Status endpoint working")
        else:
            print("    ❌ Status endpoint failed")
            results["errors"].append("Cannot retrieve system status")
        
        # Test config endpoint
        print("  ⚙️ Testing config endpoint...")
        config = self.get_config()
        if config:
            results["config"] = True
            print("    ✅ Config endpoint working")
        else:
            print("    ❌ Config endpoint failed")
            results["errors"].append("Cannot retrieve configuration")
        
        return results
    
    def monitor_systems(self, interval: int = 5, duration: int = 60):
        """Monitor system status over time"""
        print(f"📊 Monitoring systems for {duration}s (interval: {interval}s)...")
        
        start_time = time.time()
        iteration = 0
        
        while time.time() - start_time < duration:
            iteration += 1
            print(f"\n🔄 Iteration {iteration} ({time.strftime('%H:%M:%S')}):")
            
            # Quick ping test
            if self.ping():
                print("  ✅ API responding")
                
                # Get system status
                status = self.get_status()
                if status:
                    print(f"  📊 Status: {json.dumps(status, indent=2)}")
                else:
                    print("  ❌ Could not get status")
            else:
                print("  ❌ API not responding")
            
            time.sleep(interval)
        
        print(f"\n✅ Monitoring complete")
    
    def debug_system(self, system_id: str):
        """Debug a specific system"""
        print(f"🔍 Debugging system: {system_id}")
        
        systems = self.get_systems()
        if not systems:
            print("❌ Cannot retrieve systems list")
            return
        
        if system_id not in systems:
            print(f"❌ System '{system_id}' not found")
            print(f"Available systems: {', '.join(systems.keys())}")
            return
        
        system_info = systems[system_id]
        print(f"📋 System Info:")
        print(json.dumps(system_info, indent=2))
        
        # Try to get system-specific status
        try:
            response = self.session.get(f"{self.base_url}/systems/{system_id}")
            if response.status_code == 200:
                print(f"📊 System Status:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"⚠️ No specific status endpoint for {system_id}")
        except Exception as e:
            print(f"⚠️ Error getting system status: {e}")

def main():
    parser = argparse.ArgumentParser(description="SDR Cyberdeck Debug Tools")
    parser.add_argument("--host", default="localhost", help="API server host")
    parser.add_argument("--port", type=int, default=5000, help="API server port")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Ping command
    subparsers.add_parser("ping", help="Test API connectivity")
    
    # Health check command
    subparsers.add_parser("health", help="Run comprehensive health check")
    
    # Systems command
    subparsers.add_parser("systems", help="List all systems")
    
    # Status command
    subparsers.add_parser("status", help="Get system status")
    
    # Config command
    subparsers.add_parser("config", help="Get system configuration")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor systems over time")
    monitor_parser.add_argument("--interval", type=int, default=5, help="Monitoring interval (seconds)")
    monitor_parser.add_argument("--duration", type=int, default=60, help="Monitoring duration (seconds)")
    
    # Debug system command
    debug_parser = subparsers.add_parser("debug", help="Debug specific system")
    debug_parser.add_argument("system_id", help="System ID to debug")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    debugger = SDRDebugger(args.host, args.port)
    
    print(f"🔧 SDR Cyberdeck Debugger")
    print(f"📡 Target: {args.host}:{args.port}")
    print("=" * 50)
    
    if args.command == "ping":
        if debugger.ping():
            print("✅ API is responding")
        else:
            print("❌ API is not responding")
            sys.exit(1)
    
    elif args.command == "health":
        results = debugger.health_check()
        
        print("\n📋 Health Check Summary:")
        total_checks = len([k for k in results.keys() if k != "errors"])
        passed_checks = sum([v for k, v in results.items() if k != "errors"])
        
        print(f"✅ Passed: {passed_checks}/{total_checks}")
        
        if results["errors"]:
            print(f"❌ Errors:")
            for error in results["errors"]:
                print(f"  - {error}")
        
        if passed_checks == total_checks:
            print("🎉 All checks passed!")
            sys.exit(0)
        else:
            print("⚠️ Some checks failed")
            sys.exit(1)
    
    elif args.command == "systems":
        systems = debugger.get_systems()
        if systems:
            print(f"🏗️ Found {len(systems)} systems:")
            for system_id, info in systems.items():
                print(f"  - {system_id}: {info.get('name', 'No name')}")
        else:
            sys.exit(1)
    
    elif args.command == "status":
        status = debugger.get_status()
        if status:
            print("📊 System Status:")
            print(json.dumps(status, indent=2))
        else:
            sys.exit(1)
    
    elif args.command == "config":
        config = debugger.get_config()
        if config:
            print("⚙️ System Configuration:")
            print(json.dumps(config, indent=2))
        else:
            sys.exit(1)
    
    elif args.command == "monitor":
        debugger.monitor_systems(args.interval, args.duration)
    
    elif args.command == "debug":
        debugger.debug_system(args.system_id)

if __name__ == "__main__":
    main()