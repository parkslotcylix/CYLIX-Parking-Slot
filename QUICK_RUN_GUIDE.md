# Quick Run Guide - 3 Steps 🚀

**Time:** 5 minutes  
**Difficulty:** Easy

---

## 🎯 3 Simple Steps

### Step 1️⃣: Start Flask App

**Open PowerShell and run:**
```bash
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot
python app.py
```

**You should see:**
```
🚀 Starting ParkSlot Application
Running on http://127.0.0.1:5000
```

✅ **Keep this terminal open!**

---

### Step 2️⃣: Open Web Dashboard

**Open Browser and go to:**
```
http://localhost:5000
```

**You should see:**
- Parking dashboard with 3 slots
- Analytics page
- Real-time status

✅ **Dashboard is working!**

---

### Step 3️⃣: Start Master Script (Optional)

**Open new PowerShell and run:**
```bash
cd C:\Users\kydel\Downloads\ParkSlot\ParkSlot\Parking_Project
python master_script.py
```

**Then:**
1. Make sure all parking slots are EMPTY
2. Press 'c' to calibrate
3. Script will start detecting

✅ **System is running!**

---

## 🎮 Using the System

### Toggle Parking Slot
- Click on a slot card
- Status changes (Available ↔ Occupied)
- Timestamp is captured automatically

### View Analytics
- Click "Analytics" in menu
- Select time filter (Today, Yesterday, Week, Month)
- View occupancy rate and peak hours

### Print Report
- Go to Analytics page
- Select time filter
- Click "Print Report"

---

## 🛑 Stop System

**Terminal 1 (Flask):**
```
Press CTRL+C
```

**Terminal 2 (Master Script):**
```
Press 'q'
```

---

## 📊 System Status

```
✅ Flask App:        Running on http://localhost:5000
✅ Web Dashboard:    Accessible
✅ Analytics:        Real-time filtering
✅ Reports:          Filtered printing
✅ Serial Port:      COM7 available
✅ Arduino:          Connected
⏳ Camera:           Optional (needs to be powered on)
```

---

## 🔗 Useful URLs

```
Dashboard:    http://localhost:5000
Parking:      http://localhost:5000/parking
Analytics:    http://localhost:5000/analytics
Health:       http://localhost:5000/api/health
```

---

## 📞 Troubleshooting

### Flask won't start?
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Dashboard won't load?
- Check Flask app is running
- Try: `http://127.0.0.1:5000`
- Check firewall

### Master script won't connect?
- Check camera is powered on
- Verify camera is on 192.168.1.x network
- Check Arduino is connected (COM7)

---

## ✅ Done!

Your ParkSlot system is now running! 🎉

**Next:** 
- Toggle parking slots
- View analytics
- Print reports
- Monitor system

---

**Generated:** May 2, 2026
