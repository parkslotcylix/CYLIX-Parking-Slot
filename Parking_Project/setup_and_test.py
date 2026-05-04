#!/usr/bin/env python3
"""
Setup and Test Script for ParkSlot Master Script
Tests camera connection and helps find serial port
"""

import sys
import requests
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("❌ PySerial not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
    import serial
    from serial.tools import list_ports

try:
    import cv2
except ImportError:
    print("❌ OpenCV not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2

try:
    import numpy
except ImportError:
    print("❌ NumPy not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy

print("\n" + "="*70)
print("🎥 ParkSlot Master Script - Setup & Test")
print("="*70 + "\n")

# ============================================================================
# STEP 1: Test Camera Connection
# ============================================================================

print("📷 STEP 1: Testing Camera Connection")
print("-" * 70)

CAM_IP = "192.168.1.18"
CAM_URL = f"http://{CAM_IP}:81/stream"

print(f"Camera IP: {CAM_IP}")
print(f"Camera Stream URL: {CAM_URL}")

try:
    print("\n🔍 Testing camera status...")
    response = requests.get(f"http://{CAM_IP}/status", timeout=5)
    if response.status_code == 200:
        print("✅ Camera is ONLINE and responding")
        print(f"   Status: {response.text[:100]}")
    else:
        print(f"⚠️  Camera responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Cannot connect to camera at {CAM_IP}")
    print("   Make sure:")
    print("   1. ESP32 camera is powered on")
    print("   2. Camera is connected to WiFi")
    print("   3. Camera IP is correct (192.168.1.18)")
    print("   4. Your computer is on the same network")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error testing camera: {e}")
    sys.exit(1)

# ============================================================================
# STEP 2: Test Video Stream
# ============================================================================

print("\n📹 STEP 2: Testing Video Stream")
print("-" * 70)

try:
    print(f"Connecting to stream: {CAM_URL}")
    cap = cv2.VideoCapture(CAM_URL)
    
    if not cap.isOpened():
        print("❌ Cannot open video stream")
        print("   Make sure camera stream URL is correct")
        sys.exit(1)
    
    print("✅ Video stream opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print(f"✅ Successfully captured frame: {frame.shape}")
        print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
    else:
        print("⚠️  Could not read frame from stream")
    
    cap.release()
    
except Exception as e:
    print(f"❌ Error testing video stream: {e}")
    sys.exit(1)

# ============================================================================
# STEP 3: Find Serial Ports
# ============================================================================

print("\n🔌 STEP 3: Finding Serial Ports")
print("-" * 70)

ports = list(list_ports.comports())

if not ports:
    print("⚠️  No serial ports found!")
    print("   Make sure your Arduino/ESP8266 is connected via USB")
    print("   Then run this script again")
    print("\n   If you have a device connected, check:")
    print("   1. USB cable is working")
    print("   2. Device drivers are installed")
    print("   3. Device is recognized by Windows")
else:
    print(f"Found {len(ports)} serial port(s):\n")
    for i, port in enumerate(ports, 1):
        print(f"   {i}. {port.device}")
        print(f"      Description: {port.description}")
        print(f"      Manufacturer: {port.manufacturer}")
        print()

# ============================================================================
# STEP 4: Test Serial Connection (if port available)
# ============================================================================

if ports:
    print("🔗 STEP 4: Testing Serial Connection")
    print("-" * 70)
    
    selected_port = ports[0].device
    print(f"Using port: {selected_port}")
    
    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
        print(f"✅ Successfully opened serial port: {selected_port}")
        
        # Try to send test data
        test_data = "1,0,1\n"
        ser.write(test_data.encode())
        print(f"✅ Successfully sent test data: {test_data.strip()}")
        
        ser.close()
        print("✅ Serial port test successful!")
        
    except Exception as e:
        print(f"❌ Error testing serial port: {e}")
        print("   Make sure:")
        print("   1. Device is connected")
        print("   2. Correct drivers are installed")
        print("   3. No other program is using the port")

# ============================================================================
# STEP 5: Check Required Files
# ============================================================================

print("\n📁 STEP 5: Checking Required Files")
print("-" * 70)

import os

files_to_check = [
    "master_script.py",
    "slot_coords.pkl",
    "ParkingSlot.ino"
]

for filename in files_to_check:
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✅ {filename} ({size} bytes)")
    else:
        print(f"❌ {filename} NOT FOUND")

# ============================================================================
# STEP 6: Summary and Next Steps
# ============================================================================

print("\n" + "="*70)
print("📋 SUMMARY")
print("="*70)

print("\n✅ Camera: READY")
print("✅ Video Stream: READY")

if ports:
    print(f"✅ Serial Port: READY ({ports[0].device})")
    print("\n🚀 NEXT STEPS:")
    print(f"   1. Update master_script.py line 8:")
    print(f"      COM_PORT = '{ports[0].device}'")
    print(f"   2. Run: python master_script.py")
    print(f"   3. Press 'c' to calibrate (all slots must be empty)")
    print(f"   4. Press 'q' to quit")
else:
    print("⚠️  Serial Port: NOT FOUND")
    print("\n🚀 NEXT STEPS:")
    print("   1. Connect Arduino/ESP8266 via USB")
    print("   2. Run this script again to find the port")
    print("   3. Update master_script.py with the port")
    print("   4. Run: python master_script.py")

print("\n" + "="*70 + "\n")
