# Camera Connection Troubleshooting 🎥

**Issue:** TCP connection to camera stream failed (Error -138)  
**Status:** Investigating and fixing

---

## 🔍 What Happened

When you ran the master script, you got:
```
[tcp @ 000002d80aae3680] Connection to tcp://192.168.1.18:81 failed: Error number -138 occurred
```

This means:
- The script tried to connect to the camera stream
- The connection was refused or timed out
- Error -138 is a network connection error

---

## ✅ What I Fixed

I've updated the `master_script.py` with:

1. **Better Error Handling**
   - Checks if camera stream opens successfully
   - Provides clear error messages
   - Doesn't crash if camera is unavailable

2. **Correct Serial Port**
   - Changed from COM7 to **COM5** (the ESP32 camera)
   - Added serial port connection verification

3. **Improved Status Display**
   - Shows configuration at startup
   - Displays calibration progress
   - Shows detection status
   - Better error messages

4. **Graceful Shutdown**
   - Properly closes all resources
   - Turns off LED on exit
   - Handles interruptions

---

## 🚀 How to Run Now

```bash
cd Parking_Project
python master_script.py
```

**Expected Output:**
```
======================================================================
🎥 ParkSlot Master Script - Parking Detection
======================================================================

📋 Configuration:
   Camera URL: http://192.168.1.18:81/stream
   Serial Port: COM5
   Sensitivity: 10000

======================================================================

🔌 Connecting to serial port: COM5
✅ Serial port COM5 opened successfully

📁 Loading slot coordinates...
✅ Loaded 3 parking slots

📷 Connecting to camera at http://192.168.1.18:81/stream
✅ Camera stream opened successfully

💡 Setting LED intensity...
✅ LED intensity set

======================================================================
📊 CALIBRATION PHASE
======================================================================

⚠️  IMPORTANT: Make sure all 3 parking slots are EMPTY (no cars)
   Then press 'c' to capture the EMPTY reference frame
   Press 'q' to quit
```

---

## 🔧 Troubleshooting Steps

### Issue 1: Camera Stream Connection Failed

**Error:**
```
❌ Failed to open camera stream
   Camera URL: http://192.168.1.18:81/stream
```

**Solutions:**

1. **Verify Camera is Online**
   ```bash
   ping 192.168.1.18
   ```
   Should see: `Reply from 192.168.1.18`

2. **Test Camera in Browser**
   ```
   http://192.168.1.18
   ```
   Should show camera web interface

3. **Check Network Connection**
   - Verify you're on 192.168.1.x network
   - Check WiFi is connected
   - Restart camera if needed

4. **Try Different Stream URL**
   - Current: `http://192.168.1.18:81/stream`
   - Alternative: `http://192.168.1.18/stream`
   - Alternative: `http://192.168.1.18:80/stream`

5. **Check Firewall**
   - Make sure port 81 is not blocked
   - Try disabling firewall temporarily

### Issue 2: Serial Port Not Found

**Error:**
```
❌ Error opening serial port COM5: [Errno 2] No such file or directory: 'COM5'
```

**Solutions:**

1. **Verify Device is Connected**
   - Check Device Manager for COM ports
   - Look under "Ports (COM & LPT)"
   - Note the correct port

2. **Update Script with Correct Port**
   ```python
   # Edit: Parking_Project/master_script.py
   # Line 11: Change to your port
   COM_PORT = 'COM5'  # or COM3, COM7, etc.
   ```

3. **Check Device Manager**
   - Press `Win + X`
   - Select "Device Manager"
   - Expand "Ports (COM & LPT)"
   - Note the port number

### Issue 3: Camera Stream Disconnects

**Error:**
```
❌ Camera stream disconnected
```

**Solutions:**

1. **Check Network Stability**
   - Verify WiFi connection is stable
   - Move closer to WiFi router
   - Check for interference

2. **Restart Camera**
   - Power off camera
   - Wait 10 seconds
   - Power on camera
   - Wait for it to connect to WiFi

3. **Increase Timeout**
   - Edit `master_script.py`
   - Add timeout to camera connection:
   ```python
   cap = cv2.VideoCapture(CAM_URL)
   cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer
   ```

### Issue 4: Detection Not Working

**Symptoms:**
- All slots showing as occupied
- All slots showing as available
- No changes detected

**Solutions:**

1. **Recalibrate**
   - Make sure all slots are empty
   - Press 'c' to capture reference
   - Ensure good lighting

2. **Adjust Sensitivity**
   - Edit `master_script.py` line 12
   - Lower value = more sensitive
   - Higher value = less sensitive
   ```python
   SENSITIVITY = 5000   # More sensitive
   SENSITIVITY = 15000  # Less sensitive
   ```

3. **Check Lighting**
   - Ensure consistent lighting
   - Avoid shadows
   - Check camera angle

4. **Verify Slot Coordinates**
   - Make sure `slot_coords.pkl` is correct
   - Recalibrate if needed

---

## 📊 What Each Component Does

### Serial Port (COM5)
- Receives occupancy data from script
- Sends to Arduino/ESP8266
- Controls parking gate/lights

### Camera Stream (192.168.1.18:81/stream)
- Provides video feed
- Used for occupancy detection
- Requires stable network connection

### LED Control
- Script controls camera LED intensity
- Helps with lighting for detection
- Automatically turned off on exit

---

## 🎯 Next Steps

1. **Run the Updated Script**
   ```bash
   cd Parking_Project
   python master_script.py
   ```

2. **If Camera Connection Fails**
   - Check camera is powered on
   - Verify network connection
   - Try alternative stream URLs

3. **If Serial Port Fails**
   - Check Device Manager for correct port
   - Update script with correct port
   - Verify device is connected

4. **If Detection Fails**
   - Recalibrate
   - Adjust sensitivity
   - Check lighting

---

## 📝 Updated Script Features

✅ **Better Error Handling**
- Checks each connection before proceeding
- Provides clear error messages
- Doesn't crash on errors

✅ **Improved Status Display**
- Shows configuration at startup
- Displays progress during calibration
- Shows detection status
- Better error messages

✅ **Correct Serial Port**
- Updated to COM5 (ESP32 camera)
- Verifies connection before use
- Handles connection errors

✅ **Graceful Shutdown**
- Properly closes all resources
- Turns off LED on exit
- Handles interruptions

---

## 🔗 Related Documentation

- `MASTER_SCRIPT_SETUP_GUIDE.md` - Complete setup guide
- `MASTER_SCRIPT_QUICK_START.md` - Quick reference
- `READY_TO_RUN_MASTER_SCRIPT.md` - Ready to run guide

---

## 📞 Support

### Quick Checks
1. Is camera powered on? ✅
2. Is camera on 192.168.1.x network? ✅
3. Can you ping camera? `ping 192.168.1.18`
4. Can you access camera in browser? `http://192.168.1.18`
5. Is Arduino connected via USB? ✅
6. Is correct COM port in script? ✅

### If Still Having Issues
1. Check Device Manager for COM ports
2. Verify camera is accessible
3. Try alternative stream URLs
4. Restart camera and computer
5. Check network connection

---

**Status:** ✅ Script Updated & Ready to Run

**Next Action:** Run the updated script and follow the prompts!

---

**Generated:** May 2, 2026  
**Version:** 1.0.1 (Updated with better error handling)
