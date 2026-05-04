# Master Script Setup Guide 🎥

**Purpose:** Run computer vision detection on ESP32 camera to detect parking slot occupancy  
**Status:** Ready to configure and run

---

## 📋 What the Master Script Does

The `master_script.py` is a computer vision application that:

1. **Connects to ESP32 Camera** at `http://192.168.1.18:81/stream`
2. **Captures Video Stream** from the camera
3. **Detects Parking Slots** using image processing:
   - Compares current frame to empty reference
   - Calculates pixel changes in each slot area
   - Determines if slot is occupied or available
4. **Sends Results** via serial port to Arduino/ESP8266 controller
5. **Displays Live Feed** with detection overlays

---

## 🔧 Prerequisites

### Hardware
- ✅ ESP32 Camera (connected at `192.168.1.18`)
- ✅ Arduino/ESP8266 controller (on serial port)
- ✅ Computer with USB connection to controller

### Software
- ✅ Python 3.7+
- ✅ OpenCV (cv2)
- ✅ NumPy
- ✅ Requests
- ✅ PySerial

### Files
- ✅ `master_script.py` - Main script
- ✅ `slot_coords.pkl` - Parking slot coordinates (calibration data)
- ✅ `ParkingSlot.ino` - Arduino firmware

---

## 📦 Installation

### Step 1: Install Required Packages

```bash
pip install opencv-python numpy requests pyserial
```

**What each package does:**
- `opencv-python` - Computer vision library for image processing
- `numpy` - Numerical computing library
- `requests` - HTTP library for camera control
- `pyserial` - Serial communication with Arduino

### Step 2: Verify Installation

```bash
python -c "import cv2; import numpy; import requests; import serial; print('✅ All packages installed')"
```

---

## ⚙️ Configuration

### Step 1: Find Your Serial Port

**Windows:**
```powershell
# List all COM ports
Get-WmiObject Win32_SerialPort | Select-Object Name, Description

# Or check Device Manager:
# 1. Connect Arduino/ESP8266 via USB
# 2. Open Device Manager
# 3. Look under "Ports (COM & LPT)"
# 4. Note the COM port (e.g., COM5, COM3, etc.)
```

**Linux:**
```bash
# List all serial ports
ls /dev/ttyUSB* /dev/ttyACM*

# Or use dmesg
dmesg | grep tty
```

**macOS:**
```bash
# List all serial ports
ls /dev/tty.* /dev/cu.*
```

### Step 2: Update master_script.py

Edit `master_script.py` and update:

```python
# Line 8: Update COM port (Windows)
COM_PORT = 'COM5'  # Change to your actual port

# Or for Linux/macOS:
COM_PORT = '/dev/ttyUSB0'  # Or /dev/ttyACM0, /dev/cu.*, etc.

# Line 9: Adjust sensitivity if needed (optional)
SENSITIVITY = 10000  # Lower = more sensitive, Higher = less sensitive
```

### Step 3: Verify Camera URL

The script expects the camera at:
```
http://192.168.1.18:81/stream
```

**To verify camera is accessible:**
```bash
# Test camera connection
curl http://192.168.1.18/status

# Or open in browser
http://192.168.1.18
```

---

## 🚀 Running the Script

### Step 1: Start the Script

```bash
cd Parking_Project
python master_script.py
```

### Step 2: Calibration Phase

When the script starts, you'll see:
```
--- CALIBRATION ---
Make sure all 3 slots are EMPTY. Press 'c' to capture the EMPTY reference.
```

**What to do:**
1. Make sure all parking slots are **EMPTY** (no cars)
2. Press **'c'** to capture the empty reference frame
3. The script will save this as the baseline for comparison

**Expected output:**
```
Empty state saved!
Running Detection...
```

### Step 3: Detection Phase

Once calibrated, the script will:
1. Display live video feed from camera
2. Show detection rectangles around each slot:
   - **Green rectangle** = Slot is AVAILABLE
   - **Red rectangle** = Slot is OCCUPIED
3. Show pixel change count for each slot
4. Send results to Arduino via serial port

### Step 4: Stop the Script

Press **'q'** to quit the script gracefully.

---

## 📊 Understanding the Output

### Console Output
```
--- CALIBRATION ---
Make sure all 3 slots are EMPTY. Press 'c' to capture the EMPTY reference.
Empty state saved!
Running Detection...
```

### Video Display
- **Window Title:** "Parking Area"
- **Green Rectangles:** Available slots
- **Red Rectangles:** Occupied slots
- **Numbers:** Pixel change count (higher = more change)

### Serial Output
The script sends data to Arduino in format:
```
1,0,1
```
Where each number is:
- `1` = Occupied
- `0` = Available

---

## 🔍 Troubleshooting

### Issue: "Camera connection failed"
**Solution:**
1. Verify ESP32 camera is powered on
2. Check camera IP: `http://192.168.1.18`
3. Verify network connectivity
4. Check firewall isn't blocking port 81

### Issue: "Serial port not found"
**Solution:**
1. Connect Arduino/ESP8266 via USB
2. Check Device Manager for COM port
3. Update `COM_PORT` in script
4. Verify correct baud rate (115200)

### Issue: "slot_coords.pkl not found"
**Solution:**
1. Make sure you're in `Parking_Project` directory
2. Run calibration script first to generate coordinates
3. Or copy existing `slot_coords.pkl` file

### Issue: "No module named 'cv2'"
**Solution:**
```bash
pip install opencv-python
```

### Issue: "Detection not working correctly"
**Solution:**
1. Adjust `SENSITIVITY` value:
   - Lower (0-5000) = More sensitive
   - Higher (5000+) = Less sensitive
2. Recalibrate by pressing 'c' again
3. Ensure good lighting on parking area

### Issue: "Serial communication failing"
**Solution:**
1. Verify Arduino firmware is uploaded
2. Check baud rate matches (115200)
3. Test with serial monitor first
4. Verify USB cable is working

---

## 📝 Configuration Reference

### master_script.py Settings

```python
# Camera Configuration
CAM_URL = "http://192.168.1.18:81/stream"  # Camera stream URL
CAM_IP = "192.168.1.18"                     # Camera IP for LED control

# Serial Configuration
COM_PORT = 'COM5'                           # Serial port (Windows)
# COM_PORT = '/dev/ttyUSB0'                 # Serial port (Linux)
# COM_PORT = '/dev/cu.usbserial-14110'      # Serial port (macOS)

# Detection Sensitivity
SENSITIVITY = 10000  # Pixel change threshold
# Lower values = more sensitive (detects smaller changes)
# Higher values = less sensitive (requires larger changes)

# LED Intensity (0-255)
# 255 = Full brightness
# 0 = Off
```

---

## 🎯 Workflow

```
1. Start Script
   ↓
2. Calibration Phase
   - Clear all slots
   - Press 'c' to capture empty reference
   ↓
3. Detection Phase
   - Script analyzes video stream
   - Compares to empty reference
   - Detects occupied/available slots
   ↓
4. Send Results
   - Sends to Arduino via serial
   - Updates parking status
   ↓
5. Display Results
   - Shows video with overlays
   - Green = Available
   - Red = Occupied
   ↓
6. Stop Script
   - Press 'q' to quit
```

---

## 🔗 Integration with ParkSlot

The master script works with:
1. **ESP32 Camera** - Provides video stream
2. **Arduino/ESP8266** - Receives occupancy data via serial
3. **Flask App** - Can receive data from Arduino via API

**Data Flow:**
```
ESP32 Camera → master_script.py → Arduino/ESP8266 → Flask App → Web Dashboard
```

---

## 📊 Performance Tips

1. **Lighting:** Ensure good, consistent lighting on parking area
2. **Camera Angle:** Position camera to see all slots clearly
3. **Sensitivity:** Adjust based on lighting conditions
4. **Calibration:** Recalibrate if lighting changes significantly
5. **Frame Rate:** Script processes at camera's frame rate

---

## 🔒 Security Notes

- Camera stream is HTTP (not HTTPS)
- Serial communication is local only
- No authentication on camera stream
- Consider network security for production

---

## 📞 Support

### Common Issues
- Camera not connecting → Check IP and network
- Serial port errors → Verify COM port and baud rate
- Detection not working → Recalibrate and adjust sensitivity
- Performance issues → Check lighting and camera angle

### Files to Check
- `master_script.py` - Main script
- `slot_coords.pkl` - Calibration data
- `ParkingSlot.ino` - Arduino firmware

---

## ✅ Checklist Before Running

- [ ] ESP32 camera powered on and connected
- [ ] Camera accessible at `http://192.168.1.18`
- [ ] Arduino/ESP8266 connected via USB
- [ ] Serial port identified (COM5, /dev/ttyUSB0, etc.)
- [ ] Python packages installed (cv2, numpy, requests, serial)
- [ ] `slot_coords.pkl` file exists
- [ ] `master_script.py` updated with correct COM port
- [ ] All parking slots are empty for calibration
- [ ] Good lighting on parking area

---

## 🚀 Quick Start

```bash
# 1. Install packages
pip install opencv-python numpy requests pyserial

# 2. Update COM port in master_script.py
# Edit line 8: COM_PORT = 'COM5'  (change to your port)

# 3. Run script
cd Parking_Project
python master_script.py

# 4. Calibrate
# - Make sure all slots are empty
# - Press 'c' to capture reference

# 5. Monitor
# - Watch for green (available) and red (occupied) rectangles
# - Press 'q' to quit
```

---

**Status:** Ready to run!

Next: Update the COM port and run the script.
