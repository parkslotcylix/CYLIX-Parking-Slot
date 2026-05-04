# Master Script Integration Guide 🎥

**Purpose:** Integrate ESP32 camera with ParkSlot system for automated parking detection  
**Status:** Ready to configure and run  
**Date:** May 2, 2026

---

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  ParkSlot System Architecture               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ESP32 Camera (192.168.1.18)                               │
│  ├─ Captures video stream                                  │
│  ├─ Provides HTTP stream at :81/stream                     │
│  └─ Controlled via HTTP API                                │
│                                                             │
│  ↓ (Video Stream)                                          │
│                                                             │
│  master_script.py (Computer Vision)                        │
│  ├─ Connects to camera stream                              │
│  ├─ Analyzes video frames                                  │
│  ├─ Detects parking slot occupancy                         │
│  └─ Sends results via serial port                          │
│                                                             │
│  ↓ (Serial Data: 1,0,1)                                    │
│                                                             │
│  Arduino/ESP8266 (Serial Port)                             │
│  ├─ Receives occupancy data                                │
│  ├─ Controls parking gate/lights                           │
│  └─ Sends status to Flask app                              │
│                                                             │
│  ↓ (HTTP API)                                              │
│                                                             │
│  Flask App (http://localhost:5000)                         │
│  ├─ Receives parking status                                │
│  ├─ Updates database                                       │
│  ├─ Displays on web dashboard                              │
│  └─ Provides analytics                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Prerequisites

### Hardware
- ✅ ESP32 Camera (connected at 192.168.1.18)
- ✅ Arduino/ESP8266 controller (for gate/lights)
- ✅ Computer with USB connection to controller
- ✅ Network connectivity

### Software
- ✅ Python 3.7+
- ✅ OpenCV (cv2)
- ✅ NumPy
- ✅ Requests
- ✅ PySerial

### Files
- ✅ `master_script.py` - Main detection script
- ✅ `slot_coords.pkl` - Parking slot coordinates
- ✅ `ParkingSlot.ino` - Arduino firmware
- ✅ `setup_and_test.py` - Setup helper
- ✅ `find_camera.py` - Camera discovery

---

## 🚀 Quick Start (5 Minutes)

### 1. Connect to Correct Network
```
Your computer: 192.168.160.x
Camera: 192.168.1.x

⚠️ You need to connect to 192.168.1.x WiFi!
```

### 2. Verify Camera
```bash
# Open browser
http://192.168.1.18

# Or test with curl
curl http://192.168.1.18/status
```

### 3. Find Serial Port
```bash
python -m serial.tools.list_ports
# Note the COM port (e.g., COM5)
```

### 4. Update Script
Edit `Parking_Project/master_script.py`:
```python
COM_PORT = 'COM5'  # Change to your port
```

### 5. Run Script
```bash
cd Parking_Project
python master_script.py
```

### 6. Calibrate
- Make sure all slots are empty
- Press 'c' to capture reference
- Press 'q' to quit

---

## 📋 Detailed Setup

### Step 1: Network Configuration

**Current Status:**
- Your computer: `192.168.160.1` (on 192.168.160.x network)
- ESP32 camera: `192.168.1.18` (on 192.168.1.x network)

**Problem:** Different networks - can't communicate

**Solution:** Connect to same network as camera

**How to Connect:**
1. Open WiFi settings
2. Look for network that camera is on (likely "ESP32-CAM" or similar)
3. Connect to that network
4. Verify your IP is now 192.168.1.x

**Verify Connection:**
```powershell
ipconfig
# Look for IPv4 Address: 192.168.1.xxx
```

### Step 2: Test Camera Connection

Once on same network:

```bash
# Test 1: Ping camera
ping 192.168.1.18

# Test 2: Check status
curl http://192.168.1.18/status

# Test 3: Open in browser
http://192.168.1.18
```

### Step 3: Install Python Packages

```bash
pip install opencv-python numpy requests pyserial
```

**Verify Installation:**
```bash
python -c "import cv2, numpy, requests, serial; print('✅ All packages installed')"
```

### Step 4: Find Serial Port

Connect Arduino/ESP8266 via USB:

```bash
# List all serial ports
python -m serial.tools.list_ports

# Example output:
# COM3 - Arduino Uno (COM3)
# COM5 - USB Serial Device (COM5)
```

Note the port number (e.g., COM5)

### Step 5: Update master_script.py

Edit `Parking_Project/master_script.py`:

```python
# Line 8: Update COM port
COM_PORT = 'COM5'  # Change to your actual port

# Line 9: Adjust sensitivity if needed (optional)
SENSITIVITY = 10000  # Lower = more sensitive
```

### Step 6: Verify Files

Check that these files exist in `Parking_Project/`:
- ✅ `master_script.py`
- ✅ `slot_coords.pkl`
- ✅ `ParkingSlot.ino`

### Step 7: Run Setup Test

```bash
cd Parking_Project
python setup_and_test.py
```

This will:
- Test camera connection
- Test video stream
- Find serial ports
- Check required files

### Step 8: Run Master Script

```bash
cd Parking_Project
python master_script.py
```

**Expected Output:**
```
--- CALIBRATION ---
Make sure all 3 slots are EMPTY. Press 'c' to capture the EMPTY reference.
```

### Step 9: Calibrate

1. Make sure **all parking slots are EMPTY** (no cars)
2. Press **'c'** to capture the empty reference frame
3. Wait for: "Empty state saved!"
4. Script will start detection

### Step 10: Monitor Detection

The script will display:
- Live video from camera
- Green rectangles = Available slots
- Red rectangles = Occupied slots
- Pixel change count for each slot

### Step 11: Stop Script

Press **'q'** to quit gracefully

---

## 🔍 Understanding the Script

### What It Does

1. **Connects to Camera**
   - Opens video stream from `http://192.168.1.18:81/stream`
   - Captures frames at camera's frame rate

2. **Calibration Phase**
   - Captures reference frame of empty parking area
   - Converts to grayscale and applies Gaussian blur
   - Saves as baseline for comparison

3. **Detection Phase**
   - Continuously reads frames from camera
   - Compares each frame to empty reference
   - Calculates pixel changes in each slot area
   - Determines if slot is occupied or available

4. **Sends Results**
   - Formats data as: `1,0,1` (occupied, available, occupied)
   - Sends via serial port to Arduino
   - Arduino controls gate/lights based on data

5. **Displays Results**
   - Shows live video with detection overlays
   - Green rectangle = Available (0)
   - Red rectangle = Occupied (1)
   - Shows pixel change count

### Configuration Parameters

```python
# Camera
CAM_URL = "http://192.168.1.18:81/stream"  # Camera stream
CAM_IP = "192.168.1.18"                     # Camera IP

# Serial
COM_PORT = 'COM5'                           # Serial port
# Baud rate: 115200 (fixed)

# Detection
SENSITIVITY = 10000  # Pixel change threshold
# Lower (0-5000) = More sensitive
# Higher (5000+) = Less sensitive

# LED
# 255 = Full brightness
# 0 = Off
```

### Adjusting Sensitivity

If detection isn't working well:

```python
# Too many false positives (detecting empty as occupied)?
SENSITIVITY = 15000  # Increase sensitivity threshold

# Not detecting occupied slots?
SENSITIVITY = 5000   # Decrease sensitivity threshold
```

---

## 🧪 Testing

### Test 1: Camera Connection
```bash
curl http://192.168.1.18/status
# Should return camera status
```

### Test 2: Video Stream
```bash
python setup_and_test.py
# Should successfully open video stream
```

### Test 3: Serial Port
```bash
python -m serial.tools.list_ports
# Should list available COM ports
```

### Test 4: Full System
```bash
python master_script.py
# Should display calibration window
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to camera"
**Cause:** Different network or camera offline  
**Solution:**
1. Verify you're on 192.168.1.x network
2. Check camera is powered on
3. Ping camera: `ping 192.168.1.18`

### Issue: "Serial port not found"
**Cause:** Arduino not connected or wrong port  
**Solution:**
1. Connect Arduino via USB
2. Check Device Manager for COM port
3. Update `COM_PORT` in script

### Issue: "Detection not working"
**Cause:** Poor lighting or wrong sensitivity  
**Solution:**
1. Ensure good lighting on parking area
2. Recalibrate (press 'c' again)
3. Adjust `SENSITIVITY` value

### Issue: "Video stream won't open"
**Cause:** Camera stream URL incorrect  
**Solution:**
1. Verify camera IP: `http://192.168.1.18`
2. Check stream URL: `http://192.168.1.18:81/stream`
3. Test in browser first

### Issue: "No module named 'cv2'"
**Cause:** OpenCV not installed  
**Solution:**
```bash
pip install opencv-python
```

---

## 📊 Data Flow

```
ESP32 Camera
    ↓ (MJPEG Stream)
    ↓ http://192.168.1.18:81/stream
    ↓
master_script.py
    ↓ (Analyzes frames)
    ↓ (Detects occupancy)
    ↓
Arduino/ESP8266
    ↓ (Serial: 1,0,1)
    ↓ (Controls gate/lights)
    ↓
Flask App
    ↓ (HTTP API)
    ↓ (Updates database)
    ↓
Web Dashboard
    ↓ (Displays status)
    ↓
User Interface
```

---

## 🔗 Integration with ParkSlot

The master script integrates with ParkSlot by:

1. **Detecting occupancy** from camera
2. **Sending to Arduino** via serial port
3. **Arduino updates Flask app** via HTTP API
4. **Flask app updates database** with parking status
5. **Web dashboard displays** real-time status

**Data Format:**
```
Serial: "1,0,1\n"
Where: 1 = Occupied, 0 = Available

API: POST /api/toggle_slot
Body: {"slot_id": 1, "status": "occupied"}
```

---

## 📈 Performance Tips

1. **Lighting:** Ensure consistent, good lighting
2. **Camera Angle:** Position to see all slots clearly
3. **Sensitivity:** Adjust based on lighting conditions
4. **Calibration:** Recalibrate if lighting changes
5. **Frame Rate:** Script processes at camera's FPS

---

## 🔒 Security Notes

- Camera stream is HTTP (not HTTPS)
- Serial communication is local only
- No authentication on camera
- Consider network security for production

---

## 📁 File Structure

```
Parking_Project/
├── master_script.py          # Main detection script
├── setup_and_test.py         # Setup helper
├── find_camera.py            # Camera discovery
├── slot_coords.pkl           # Calibration data
├── ParkingSlot.ino           # Arduino firmware
└── data/                     # Data directory
```

---

## ✅ Checklist

- [ ] Computer on 192.168.1.x network
- [ ] Camera accessible at 192.168.1.18
- [ ] Python packages installed
- [ ] Arduino/ESP8266 connected via USB
- [ ] Serial port identified
- [ ] `master_script.py` updated with COM port
- [ ] `slot_coords.pkl` exists
- [ ] All parking slots empty for calibration
- [ ] Good lighting on parking area

---

## 🚀 Next Steps

1. **Connect to 192.168.1.x WiFi**
2. **Verify camera at `http://192.168.1.18`**
3. **Install Python packages**
4. **Find serial port**
5. **Update `master_script.py`**
6. **Run `python master_script.py`**
7. **Calibrate by pressing 'c'**
8. **Monitor detection results**

---

## 📞 Support

### Quick Commands
```bash
# Check IP
ipconfig

# Find serial ports
python -m serial.tools.list_ports

# Test camera
curl http://192.168.1.18/status

# Run setup test
python setup_and_test.py

# Run master script
python master_script.py
```

### Documentation Files
- `MASTER_SCRIPT_SETUP_GUIDE.md` - Detailed setup
- `MASTER_SCRIPT_QUICK_START.md` - Quick reference
- `MASTER_SCRIPT_INTEGRATION_GUIDE.md` - This file

---

**Status:** ✅ Ready to run!

**Next:** Connect to 192.168.1.x WiFi and follow the Quick Start guide.

---

**Generated:** May 2, 2026  
**Version:** 1.0.0  
**System:** ParkSlot with ESP32 Camera Integration
