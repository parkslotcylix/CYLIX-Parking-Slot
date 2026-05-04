# Master Script - Camera Offline Guide 📋

**Status:** Camera not responding  
**Solution:** Run script in test mode or fix camera connection

---

## 🔍 What's Happening

The camera at `192.168.1.18` is not responding:
- ❌ Ping timeout
- ❌ HTTP connection timeout
- ❌ Stream connection failed

**Possible Causes:**
1. Camera is powered off
2. Camera is not on the network
3. Camera IP changed
4. Network connectivity issue

---

## 🔧 Option 1: Fix Camera Connection

### Step 1: Check Camera Power
- Verify camera is powered on
- Check LED indicators
- Look for WiFi connection light

### Step 2: Check Network
- Verify camera is on 192.168.1.x network
- Check WiFi connection
- Try accessing: `http://192.168.1.18` in browser

### Step 3: Restart Camera
1. Power off camera
2. Wait 10 seconds
3. Power on camera
4. Wait for WiFi connection (30-60 seconds)
5. Try again

### Step 4: Find Camera IP
If camera IP changed, find it:
```bash
# Run network scan
cd Parking_Project
python find_camera.py
```

### Step 5: Update Script
If you find a different IP:
```python
# Edit: Parking_Project/master_script.py
# Line 9: Update camera IP
CAM_IP = "192.168.1.XX"  # New IP
CAM_URL = "http://192.168.1.XX:81/stream"
```

---

## 🔧 Option 2: Run Script in Test Mode

If camera is offline but you want to test the serial communication:

### Create Test Script
```python
# Parking_Project/test_master_script.py
import serial
import time

COM_PORT = 'COM7'
ser = serial.Serial(COM_PORT, 115200, timeout=0.1)

print("Testing serial communication...")
print("Sending test data to Arduino...\n")

# Send test data
test_data = [
    "1,0,1",  # Slot 1 occupied, Slot 2 available, Slot 3 occupied
    "0,1,0",  # Slot 1 available, Slot 2 occupied, Slot 3 available
    "1,1,1",  # All occupied
    "0,0,0",  # All available
]

for data in test_data:
    print(f"Sending: {data}")
    ser.write(f"{data}\n".encode())
    time.sleep(1)

ser.close()
print("Test complete!")
```

### Run Test Script
```bash
cd Parking_Project
python test_master_script.py
```

---

## 🔧 Option 3: Create Fallback Script

If camera won't connect, create a manual input script:

```python
# Parking_Project/manual_detection.py
import serial
import time

COM_PORT = 'COM7'
ser = serial.Serial(COM_PORT, 115200, timeout=0.1)

print("Manual Parking Detection")
print("Enter slot status (1=occupied, 0=available)")
print("Format: slot1,slot2,slot3")
print("Example: 1,0,1")
print("Type 'quit' to exit\n")

while True:
    try:
        data = input("Enter status: ")
        
        if data.lower() == 'quit':
            break
        
        # Validate format
        parts = data.split(',')
        if len(parts) != 3:
            print("Invalid format. Use: slot1,slot2,slot3")
            continue
        
        # Validate values
        if not all(p in ['0', '1'] for p in parts):
            print("Invalid values. Use 0 or 1 only")
            continue
        
        # Send to Arduino
        ser.write(f"{data}\n".encode())
        print(f"✅ Sent: {data}\n")
    
    except Exception as e:
        print(f"Error: {e}\n")

ser.close()
print("Done!")
```

### Run Manual Script
```bash
cd Parking_Project
python manual_detection.py
```

---

## 📋 Checklist

### Camera Connection
- [ ] Camera is powered on
- [ ] Camera is on 192.168.1.x network
- [ ] Camera is accessible at `http://192.168.1.18`
- [ ] Camera stream works at `http://192.168.1.18:81/stream`

### Serial Connection
- [ ] Arduino/ESP8266 connected via USB
- [ ] Serial port COM7 is available
- [ ] Serial communication working

### Master Script
- [ ] Camera URL correct
- [ ] Serial port correct
- [ ] Slot coordinates loaded
- [ ] Script runs without errors

---

## 🚀 Next Steps

### If Camera is Offline
1. Power on camera
2. Wait for WiFi connection
3. Verify at `http://192.168.1.18`
4. Run master script again

### If Camera IP Changed
1. Run `python find_camera.py`
2. Find new IP
3. Update `master_script.py`
4. Run script again

### If You Want to Test Serial Only
1. Run `python test_master_script.py`
2. Or run `python manual_detection.py`
3. Verify Arduino receives data

---

## 📞 Support

### Quick Checks
1. Is camera powered on? ✅
2. Is camera on 192.168.1.x network? ✅
3. Can you access `http://192.168.1.18` in browser? ✅
4. Is Arduino connected via USB? ✅
5. Is COM7 available? ✅

### If Camera Still Not Working
1. Restart camera
2. Check WiFi connection
3. Try different IP
4. Check network connectivity
5. Restart computer

---

## 📊 Summary

**Current Status:**
- ❌ Camera: Not responding
- ✅ Serial Port: COM7 available
- ✅ Arduino: Connected

**Options:**
1. Fix camera connection (recommended)
2. Test serial communication only
3. Use manual input script

**Recommended:** Fix camera connection first, then run master script

---

**Generated:** May 2, 2026  
**Status:** Troubleshooting
