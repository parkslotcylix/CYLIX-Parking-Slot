#!/usr/bin/env python3
"""
Test Camera Connection
Tries different URLs and methods to connect to the camera
"""

import requests
import cv2
import time

print("\n" + "="*70)
print("🎥 Testing Camera Connection")
print("="*70 + "\n")

CAM_IP = "192.168.1.18"

# Test 1: Ping camera
print("Test 1: Ping camera")
import subprocess
try:
    result = subprocess.run(['ping', '-n', '1', CAM_IP], capture_output=True, timeout=2)
    if result.returncode == 0:
        print(f"✅ Camera is reachable at {CAM_IP}\n")
    else:
        print(f"❌ Camera is not reachable at {CAM_IP}\n")
except Exception as e:
    print(f"⚠️  Ping failed: {e}\n")

# Test 2: HTTP status
print("Test 2: HTTP Status")
try:
    response = requests.get(f"http://{CAM_IP}/status", timeout=2)
    print(f"✅ HTTP Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}\n")
except Exception as e:
    print(f"❌ HTTP Status failed: {e}\n")

# Test 3: Try different stream URLs
print("Test 3: Testing different stream URLs\n")

stream_urls = [
    f"http://{CAM_IP}:81/stream",
    f"http://{CAM_IP}:80/stream",
    f"http://{CAM_IP}/stream",
    f"http://{CAM_IP}:81/video_feed",
    f"http://{CAM_IP}/video_feed",
    f"http://{CAM_IP}:81/mjpeg",
    f"http://{CAM_IP}/mjpeg",
]

for url in stream_urls:
    print(f"Trying: {url}")
    try:
        cap = cv2.VideoCapture(url)
        time.sleep(1)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"   ✅ SUCCESS! Stream opened and frame captured")
                print(f"   Frame size: {frame.shape}")
                cap.release()
                print(f"\n🎉 Use this URL in master_script.py:")
                print(f"   CAM_URL = \"{url}\"\n")
                break
            else:
                print(f"   ⚠️  Stream opened but no frame")
                cap.release()
        else:
            print(f"   ❌ Failed to open stream")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

# Test 4: Check camera web interface
print("\nTest 4: Camera Web Interface")
try:
    response = requests.get(f"http://{CAM_IP}/", timeout=2)
    if response.status_code == 200:
        print(f"✅ Camera web interface is accessible")
        print(f"   Open in browser: http://{CAM_IP}/\n")
    else:
        print(f"❌ Camera web interface returned: {response.status_code}\n")
except Exception as e:
    print(f"❌ Camera web interface error: {e}\n")

print("="*70)
print("🎯 Summary")
print("="*70)
print("\nIf a stream URL worked above, update master_script.py:")
print("   CAM_URL = \"<working_url>\"")
print("\nIf no URLs worked:")
print("   1. Check camera is powered on")
print("   2. Check camera is on 192.168.1.x network")
print("   3. Try accessing http://192.168.1.18 in browser")
print("   4. Restart camera if needed")
print("\n" + "="*70 + "\n")
