#!/usr/bin/env python3
"""
Find ESP32 Camera on Network
Scans local network for the camera
"""

import subprocess
import sys
import re
from ipaddress import ip_network, ip_address

print("\n" + "="*70)
print("🔍 Finding ESP32 Camera on Network")
print("="*70 + "\n")

# Get local network info
try:
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    output = result.stdout
    
    # Find IPv4 addresses
    ipv4_pattern = r'IPv4 Address.*?:\s+(\d+\.\d+\.\d+\.\d+)'
    matches = re.findall(ipv4_pattern, output)
    
    if matches:
        local_ip = matches[0]
        print(f"Your IP: {local_ip}")
        
        # Extract network (assuming /24 subnet)
        parts = local_ip.split('.')
        network = f"{parts[0]}.{parts[1]}.{parts[2]}"
        print(f"Network: {network}.0/24\n")
        
        print("Scanning for devices...\n")
        
        # Scan network
        found_devices = []
        for i in range(1, 255):
            ip = f"{network}.{i}"
            
            # Use ping to check if device is online
            try:
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '100', ip],
                    capture_output=True,
                    text=True,
                    timeout=1
                )
                
                if result.returncode == 0:
                    found_devices.append(ip)
                    print(f"✅ Found device: {ip}")
                    
                    # Try to identify if it's the camera
                    try:
                        import requests
                        response = requests.get(f"http://{ip}/status", timeout=1)
                        if response.status_code == 200:
                            print(f"   ✅ This is the ESP32 CAMERA!")
                            print(f"   Stream URL: http://{ip}:81/stream")
                    except:
                        pass
                    
            except:
                pass
        
        if found_devices:
            print(f"\n✅ Found {len(found_devices)} device(s) on network")
            print("\nTo identify which is the camera:")
            print("1. Open browser and visit: http://<IP>")
            print("2. Look for ESP32 camera web interface")
            print("3. Update master_script.py with the correct IP")
        else:
            print("❌ No devices found on network")
            print("\nMake sure:")
            print("1. ESP32 camera is powered on")
            print("2. Camera is connected to WiFi")
            print("3. Camera is on the same network as your computer")
    
    else:
        print("❌ Could not find your IP address")
        print("Make sure you're connected to a network")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nAlternative: Check your router's connected devices list")
    print("Look for a device named 'ESP32' or similar")

print("\n" + "="*70 + "\n")
