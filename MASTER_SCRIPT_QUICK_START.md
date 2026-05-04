# Master Script - Quick Start Guide 🚀

**Status:** Ready to run  
**Camera:** ESP32 at `192.168.1.18` (already connected)  
**Next:** Configure and run the script

---

## ⚠️ Network Issue Detected

Your computer is on network: `192.168.160.x`  
The camera is on network: `192.168.1.x`

**Solution:** Connect your computer to the same network as the camera (192.168.1.x WiFi)

---

## 🔧 Setup Steps

### Step 1: Connect to Same Network

1. **Disconnect** from current WiFi (192.168.160.x)
2. **Connect** to the same WiFi network as the ESP32 camera (192.168.1.x)
3. **Verify** your IP is now in 192.168.1.x range

**To check your IP:**
```powershell
ipconfig
```

Look for IPv4 Address like: `192.168.1.xxx`

### Step 2: Verify Camera Connection

Once on the same network, test camera:

```bash
# Test camera status
curl http://192.168.1.18/status

# Or open in browser
http://192.168.1.18
```

### Step 3: Find Serial Port

Connect your Arduino/ESP8266 via USB, then run:

```bash
cd Parking_Project
python -m serial.tools.list_ports
```

Note the COM port (e.g., COM3, COM5, etc.)

### Step 4: Update master_script.py

Edit `Parking_Project/master_script.py` and update:

```python
# Line 8: Update COM port
COM_PORT = 'COM5'  # Change to your actual port from Step 3
```

### Step 5: Run the Script

```bash
cd Parking_Project
python master_script.py
```

### Step 6: Calibrate

When you see:
```
--- CALIBRATION ---
Make sure all 3 slots are EMPTY. Press 'c' to capture the EMPTY reference.
```

1. Make sure all parking slots are **EMPTY**
2. Press **'c'** to capture the reference
3. Wait for "Empty state saved!"

### Step 7: Monitor Detection

The script will now:
- Display live video from camera
- Show green rectangles for available slots
- Show red rectangles for occupied slots
- Send data to Arduino via serial port

### Step 8: Stop Script

Press **'q'** to quit gracefully

---

## 📋 Checklist

- [ ] Computer connected to 192.168.1.x WiFi
- [ ] Camera accessible at `http://192.168.1.18`
- [ ] Arduino/ESP8266 connected via USB
- [ ] Serial port identified (COM3, COM5, etc.)
- [ ] `master_script.py` updated with correct COM port
- [ ] All parking slots empty for calibration
- [ ] Good lighting on parking area

---

## 🚀 Quick Commands

```bash
# Check your IP
ipconfig

# Find serial ports
python -m serial.tools.list_ports

# Run setup and test
cd Parking_Project
python setup_and_test.py

# Run master script
python master_script.py
```

---

## 📞 Troubleshooting

### Camera not responding
- Verify you're on 192.168.1.x network
- Check camera is powered on
- Try: `http://192.168.1.18` in browser

### Serial port not found
- Connect Arduino/ESP8266 via USB
- Check Device Manager for COM port
- Run: `python -m serial.tools.list_ports`

### Detection not working
- Recalibrate (press 'c' again)
- Adjust SENSITIVITY in script
- Ensure good lighting

---

## 📊 What Happens When Running

```
1. Script connects to camera at 192.168.1.18:81/stream
2. Displays calibration window
3. You press 'c' to capture empty reference
4. Script analyzes video stream
5. Detects occupied/available slots
6. Sends results to Arduino via serial port
7. Displays live video with detection overlays
8. Press 'q' to quit
```

---

## 🎯 Next Steps

1. **Connect to 192.168.1.x WiFi**
2. **Verify camera at `http://192.168.1.18`**
3. **Find serial port**
4. **Update `master_script.py` with COM port**
5. **Run `python master_script.py`**
6. **Calibrate by pressing 'c'**
7. **Monitor detection results**

---

**Ready to go! Just connect to the right WiFi network first.** 🎉
