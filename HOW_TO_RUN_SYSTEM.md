# How to Run ParkSlot System - Complete Guide 🚀

**Status:** Ready to run  
**Time to complete:** 5-10 minutes

---

## 📋 System Overview

Your ParkSlot system has 3 main components:

```
1. Flask Web App (http://localhost:5000)
   ├─ Web dashboard
   ├─ Analytics
   └─ API endpoints

2. Master Script (Computer Vision)
   ├─ Connects to ESP32 camera
   ├─ Detects parking occupancy
   └─ Sends to Arduino

3. Arduino/ESP8266 (Serial Port COM7)
   ├─ Receives occupancy data
   ├─ Controls gate/lights
   └─ Manages hardware
```

---

## 🎯 Quick Start (5 minutes)

### Step 1: Start Flask App

**Open Terminal 1:**
```bash
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot
python app.py
```

**Expected Output:**
```
🚀 Starting ParkSlot Application
Environment: production
Host: 0.0.0.0
Port: 5000
Running on http://127.0.0.1:5000
```

**✅ Flask app is now running!**

### Step 2: Open Web Dashboard

**Open Browser:**
```
http://localhost:5000
```

**You should see:**
- Parking dashboard with 3 slots
- Analytics page
- Real-time status

**✅ Web dashboard is working!**

### Step 3: Start Master Script (Optional)

**Open Terminal 2:**
```bash
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot\Parking_Project
python master_script.py
```

**Expected Output:**
```
🎥 ParkSlot Master Script - Parking Detection
Serial Port: COM7
Camera URL: http://192.168.1.18:81/stream

🔌 Connecting to serial port: COM7
✅ Serial port COM7 opened successfully

📷 Connecting to camera...
```

**Note:** Camera needs to be powered on and on the network

**✅ Master script is running!**

---

## 📊 Detailed Instructions

### Part 1: Start Flask Web App

#### Windows PowerShell

```powershell
# Navigate to project directory
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot

# Run Flask app
python app.py
```

#### Expected Output
```
Password reset table check skipped at startup
======================================================================
🚀 Starting ParkSlot Application
======================================================================
Environment: production
Debug Mode: False
Host: 0.0.0.0
Port: 5000
Database: Supabase REST API
======================================================================
✅ Access your app at:
   Local:        http://localhost:5000
   Local Network: http://192.168.1.9:5000
   Health Check: http://localhost:5000/api/health
======================================================================
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.9:5000
Press CTRL+C to quit
```

#### ✅ Flask App is Running!

**Keep this terminal open!**

---

### Part 2: Access Web Dashboard

#### Open Browser

```
http://localhost:5000
```

#### What You'll See

**Home Page:**
- ParkSlot logo
- Navigation menu
- Quick links

**Parking Dashboard:**
- 3 parking slots
- Real-time status (Available/Occupied)
- Summary cards (Total, Available, Occupied)
- Time display

**Analytics Dashboard:**
- Time filters (Today, Yesterday, Week, Month)
- Occupancy rate
- Peak hours
- Session data
- Print report button

#### ✅ Web Dashboard is Working!

---

### Part 3: Start Master Script (Optional)

#### Prerequisites

Before running master script, make sure:
- [ ] ESP32 camera is powered on
- [ ] Camera is on 192.168.1.x network
- [ ] Arduino/ESP8266 is connected via USB (COM7)
- [ ] Flask app is running (Terminal 1)

#### Open New Terminal (Terminal 2)

```powershell
# Navigate to Parking_Project
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot\Parking_Project

# Run master script
python master_script.py
```

#### Expected Output

```
======================================================================
🎥 ParkSlot Master Script - Parking Detection
======================================================================

📋 Configuration:
   Camera URL: http://192.168.1.18:81/stream
   Serial Port: COM7
   Sensitivity: 10000

======================================================================

🔌 Connecting to serial port: COM7
✅ Serial port COM7 opened successfully

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

#### Calibration Steps

1. **Make sure all parking slots are EMPTY** (no cars)
2. **Press 'c'** to capture the empty reference
3. **Wait for:** "Empty state saved!"
4. Script will start detection

#### Detection Phase

```
======================================================================
🚀 DETECTION PHASE - Running
======================================================================

📊 Status:
   🟢 Green rectangle = Available slot
   🔴 Red rectangle = Occupied slot
   Press 'q' to quit

   Frame 30: Slot 1=Available, Data sent: 0,0,0
   Frame 60: Slot 1=Occupied, Data sent: 1,0,0
```

#### ✅ Master Script is Running!

**Keep this terminal open!**

---

## 🎮 Using the System

### Parking Dashboard

**Toggle Slot Status:**
1. Click on a parking slot card
2. Status changes (Available ↔ Occupied)
3. Timestamp is captured automatically
4. Data is sent to database

**View Summary:**
- Total slots: 3
- Available: Shows available count
- Occupied: Shows occupied count

### Analytics Dashboard

**Select Time Filter:**
1. Click filter button (Today, Yesterday, Week, Month)
2. Data updates automatically
3. Shows occupancy rate
4. Shows peak hours

**Print Report:**
1. Click "Print Report" button
2. Report shows filtered data
3. Includes all parking history for selected period

### API Endpoints

**Test endpoints:**
```bash
# Get all slots
curl http://localhost:5000/api/get_slots

# Get analytics
curl http://localhost:5000/api/analytics/sessions?filter=today

# Health check
curl http://localhost:5000/api/health
```

---

## 🛑 Stopping the System

### Stop Flask App

**In Terminal 1:**
```
Press CTRL+C
```

**Expected Output:**
```
^C
Keyboard interrupt received, exiting.
```

### Stop Master Script

**In Terminal 2:**
```
Press 'q'
```

**Expected Output:**
```
✅ Detection stopped by user
======================================================================
🛑 Shutting down...
======================================================================
✅ LED turned off
✅ All resources closed
======================================================================
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ParkSlot System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Terminal 1: Flask App                                      │
│  ├─ http://localhost:5000                                  │
│  ├─ Web dashboard                                          │
│  ├─ Analytics                                              │
│  └─ API endpoints                                          │
│                                                             │
│  Terminal 2: Master Script (Optional)                       │
│  ├─ ESP32 Camera (192.168.1.18)                            │
│  ├─ Computer Vision Detection                              │
│  ├─ Serial Communication (COM7)                            │
│  └─ Arduino/ESP8266 Control                                │
│                                                             │
│  Browser: Web Interface                                     │
│  ├─ Parking Dashboard                                      │
│  ├─ Analytics Dashboard                                    │
│  └─ Reports                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Troubleshooting

### Issue: Flask App Won't Start

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Try again
python app.py
```

### Issue: Master Script Won't Connect to Camera

**Error:**
```
❌ Failed to open camera stream
```

**Solution:**
1. Check camera is powered on
2. Verify camera is on 192.168.1.x network
3. Try: `http://192.168.1.18` in browser
4. Restart camera if needed

### Issue: Serial Port Not Found

**Error:**
```
❌ Error opening serial port COM7
```

**Solution:**
1. Check Arduino is connected via USB
2. Verify COM7 in Device Manager
3. Update script if port is different

### Issue: Web Dashboard Not Loading

**Error:**
```
Cannot connect to localhost:5000
```

**Solution:**
1. Check Flask app is running (Terminal 1)
2. Verify port 5000 is not blocked
3. Try: `http://127.0.0.1:5000`
4. Check firewall settings

---

## 📋 Checklist

### Before Running

- [ ] Python 3.7+ installed
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file configured
- [ ] `slot_coords.pkl` exists
- [ ] Arduino connected (optional)
- [ ] Camera powered on (optional)

### Running Flask App

- [ ] Terminal 1 open
- [ ] Flask app started: `python app.py`
- [ ] Output shows "Running on..."
- [ ] No errors in console

### Using Web Dashboard

- [ ] Browser opened: `http://localhost:5000`
- [ ] Dashboard loads
- [ ] Parking slots visible
- [ ] Can toggle slots
- [ ] Analytics page works

### Running Master Script (Optional)

- [ ] Terminal 2 open
- [ ] Master script started: `python master_script.py`
- [ ] Serial port connected
- [ ] Camera connected
- [ ] Calibration complete

---

## 🎯 Common Tasks

### Task 1: View Parking Status

1. Open browser: `http://localhost:5000`
2. Go to Parking Dashboard
3. See all 3 slots with status
4. View summary (Total, Available, Occupied)

### Task 2: Toggle Parking Slot

1. Click on a slot card
2. Status changes (Available ↔ Occupied)
3. Timestamp is captured
4. Data is saved to database

### Task 3: View Analytics

1. Click "Analytics" in menu
2. Select time filter (Today, Yesterday, Week, Month)
3. View occupancy rate
4. View peak hours
5. View session data

### Task 4: Print Report

1. Go to Analytics page
2. Select time filter
3. Click "Print Report"
4. Report shows all data for selected period
5. Print or save as PDF

### Task 5: Check System Health

1. Open browser
2. Visit: `http://localhost:5000/api/health`
3. Should show: `{"status": "healthy", "database": "connected"}`

---

## 📊 Performance Tips

1. **Keep Flask app running** - Don't close Terminal 1
2. **Use Chrome/Firefox** - Better performance
3. **Refresh page** - If data doesn't update
4. **Check console** - For error messages
5. **Monitor resources** - Check CPU/Memory usage

---

## 🔗 Useful URLs

```
Home:              http://localhost:5000
Parking:           http://localhost:5000/parking
Analytics:         http://localhost:5000/analytics
Health Check:      http://localhost:5000/api/health
API Slots:         http://localhost:5000/api/get_slots
API Analytics:     http://localhost:5000/api/analytics/sessions?filter=today
```

---

## 📞 Quick Reference

### Start System
```bash
# Terminal 1: Flask App
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot
python app.py

# Terminal 2: Master Script (Optional)
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot\Parking_Project
python master_script.py
```

### Stop System
```bash
# Terminal 1: Press CTRL+C
# Terminal 2: Press 'q'
```

### Access Dashboard
```
http://localhost:5000
```

---

## ✅ Summary

**To run the complete ParkSlot system:**

1. **Terminal 1:** `python app.py` (Flask app)
2. **Browser:** `http://localhost:5000` (Web dashboard)
3. **Terminal 2:** `python master_script.py` (Master script - optional)

**That's it! System is running!** 🎉

---

**Generated:** May 2, 2026  
**Status:** Ready to Run
