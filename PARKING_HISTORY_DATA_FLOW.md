# Parking History System - Complete Data Flow

## Overview

This document explains how data flows through the parking history system from slot toggle to analytics report.

---

## 1. Slot Toggle Flow

### User Action: Click Parking Slot

```
User clicks slot on /parking page
    ↓
JavaScript sends POST to /api/toggle_slot
    ↓
Backend receives request with slot_id
    ↓
Check current slot status in parking_slots table
```

### Case A: Slot is AVAILABLE → Toggle to OCCUPIED

```
Current Status: Available
    ↓
UPDATE parking_slots:
  - slot_status = 'Occupied'
  - check_in_time = NOW()
  - updated_at = NOW()
    ↓
INSERT INTO parking_history:
  - slot_id = [slot_id]
  - check_in_time = NOW()
  - status = 'active'
  - created_at = NOW()
    ↓
INSERT INTO admin_logs:
  - action = 'toggle_slot'
  - slot_id = [slot_id]
  - description = 'Status changed to Occupied'
    ↓
Return JSON response:
  {
    "success": true,
    "new_status": "Occupied",
    "timestamp": "2026-05-02 01:30:39"
  }
    ↓
Frontend updates UI to show slot as occupied
```

### Case B: Slot is OCCUPIED → Toggle to AVAILABLE

```
Current Status: Occupied
    ↓
UPDATE parking_slots:
  - slot_status = 'Available'
  - check_out_time = NOW()
  - updated_at = NOW()
    ↓
SELECT FROM parking_history:
  - Find active record for this slot
  - WHERE slot_id = [slot_id] AND status = 'active'
  - ORDER BY history_id DESC LIMIT 1
    ↓
Calculate duration:
  - duration_hours = (check_out_time - check_in_time) / 3600
    ↓
UPDATE parking_history:
  - check_out_time = NOW()
  - status = 'completed'
  - duration_hours = [calculated]
  - WHERE history_id = [history_id]
    ↓
INSERT INTO admin_logs:
  - action = 'toggle_slot'
  - slot_id = [slot_id]
  - description = 'Status changed to Available'
    ↓
Return JSON response:
  {
    "success": true,
    "new_status": "Available",
    "timestamp": "2026-05-02 01:30:44"
  }
    ↓
Frontend updates UI to show slot as available
```

---

## 2. Analytics Data Collection Flow

### User Navigates to /analytics

```
User visits http://localhost:5000/analytics
    ↓
Page loads templates/analytics.html
    ↓
JavaScript runs loadAnalytics() function
    ↓
Three parallel API calls:
```

### Call 1: Get Sessions Statistics

```
fetch('/api/analytics/sessions')
    ↓
Backend executes:
  SELECT COUNT(*) as total_sessions 
  FROM parking_history 
  WHERE status = 'completed'
    ↓
  SELECT COUNT(*) as active_sessions 
  FROM parking_history 
  WHERE status = 'active'
    ↓
  SELECT COALESCE(AVG(duration_hours), 0) as avg_duration 
  FROM parking_history 
  WHERE status = 'completed' AND duration_hours IS NOT NULL
    ↓
Return JSON:
  {
    "success": true,
    "total_sessions": 2,
    "active_sessions": 3,
    "average_duration": 0.0
  }
    ↓
Frontend updates cards:
  - "Total Sessions Completed": 2
  - "Avg. Parking Duration": 0h 0m
  - "Active Sessions": 3 Active
```

### Call 2: Get Hourly Statistics

```
fetch('/api/analytics/hourly')
    ↓
Backend executes:
  SELECT EXTRACT(HOUR FROM check_in_time) as hour,
         COUNT(*) as count
  FROM parking_history
  WHERE DATE(check_in_time) = TODAY()
  GROUP BY EXTRACT(HOUR FROM check_in_time)
  ORDER BY hour
    ↓
Return JSON:
  {
    "success": true,
    "hourly_stats": [0, 0, 0, ..., 2, 1, 0, ...]
  }
    ↓
Frontend creates Chart.js line chart:
  - X-axis: Hours (12a, 1a, 2a, ..., 11p)
  - Y-axis: Occupancy percentage
  - Displays 24-hour occupancy pattern
```

### Call 3: Get Parking Summary

```
fetch('/api/get_summary')
    ↓
Backend executes:
  SELECT COUNT(*) as total,
         SUM(CASE WHEN slot_status = 'Available' THEN 1 ELSE 0 END) as available,
         SUM(CASE WHEN slot_status = 'Occupied' THEN 1 ELSE 0 END) as occupied
  FROM parking_slots
    ↓
Return JSON:
  {
    "success": true,
    "summary": {
      "total": 3,
      "available": 0,
      "occupied": 3,
      "occupancy_percent": 100
    }
  }
    ↓
Frontend updates card:
  - "Available Parking Slots": 0/3
```

---

## 3. Print Report Generation Flow

### User Clicks "Print Analytics Report"

```
User clicks button
    ↓
JavaScript calls printAnalyticsReport()
    ↓
Fetch current data from page:
  - totalSessions = document.getElementById('ac-vehicles').textContent
  - avgDuration = document.getElementById('ac-duration').textContent
  - slotsInfo = document.getElementById('analytics-slots-num').textContent
  - activeSessions = document.getElementById('ac-active-sessions').textContent
    ↓
fetch('/api/get_history')
    ↓
Backend executes:
  SELECT * FROM parking_history
  ORDER BY history_id DESC
  LIMIT 100
    ↓
Return JSON:
  {
    "success": true,
    "history": [
      {
        "history_id": 5,
        "slot_id": 1,
        "check_in_time": "2026-05-02 01:25:27",
        "check_out_time": null,
        "duration_hours": null,
        "status": "active",
        "created_at": "2026-05-02 01:25:27"
      },
      ...
    ]
  }
    ↓
Frontend generates HTML report:
  - Header with logo and date
  - Executive summary
  - Key metrics cards
  - History table (last 10 records)
  - Footer with copyright
    ↓
Open new window with report HTML
    ↓
User sees professional PDF-ready report
    ↓
User clicks print (Ctrl+P)
    ↓
Browser prints or saves as PDF
```

---

## 4. Database Schema Relationships

```
parking_slots
├── slot_id (PK)
├── slot_number
├── slot_status (Available/Occupied/Maintenance)
├── check_in_time
├── check_out_time
├── vehicle_reg_number
└── updated_at

        ↓ (Foreign Key)

parking_history
├── history_id (PK)
├── slot_id (FK → parking_slots.slot_id)
├── vehicle_reg_number
├── check_in_time
├── check_out_time
├── duration_hours (calculated)
├── parking_fee
├── status (active/completed/cancelled)
├── notes
└── created_at

        ↓ (Audit Trail)

admin_logs
├── log_id (PK)
├── admin_id
├── action (toggle_slot)
├── slot_id
├── description
└── created_at
```

---

## 5. Real-Time Update Cycle

```
Page loads
    ↓
loadAnalytics() called
    ↓
All API calls executed
    ↓
Data displayed on page
    ↓
Wait 10 seconds
    ↓
setInterval(loadAnalytics, 10000) triggers
    ↓
All API calls executed again
    ↓
Data refreshed on page
    ↓
Repeat every 10 seconds
```

---

## 6. Example: Complete Parking Session

### Timeline

```
01:25:27 - User clicks slot 1
  ├─ POST /api/toggle_slot {slot_id: 1}
  ├─ parking_slots: UPDATE slot_status='Occupied', check_in_time='01:25:27'
  ├─ parking_history: INSERT (slot_id=1, check_in_time='01:25:27', status='active')
  ├─ admin_logs: INSERT (action='toggle_slot', description='Status changed to Occupied')
  └─ Response: {success: true, new_status: 'Occupied'}

01:25:35 - Analytics page auto-refreshes
  ├─ GET /api/analytics/sessions
  ├─ Query: SELECT COUNT(*) FROM parking_history WHERE status='active'
  ├─ Result: active_sessions = 1
  └─ Display: "1 Active"

01:30:44 - User clicks slot 1 again
  ├─ POST /api/toggle_slot {slot_id: 1}
  ├─ parking_slots: UPDATE slot_status='Available', check_out_time='01:30:44'
  ├─ parking_history: SELECT WHERE slot_id=1 AND status='active'
  ├─ Calculate: duration_hours = (01:30:44 - 01:25:27) / 3600 = 0.0048 hours
  ├─ parking_history: UPDATE status='completed', check_out_time='01:30:44', duration_hours=0.0048
  ├─ admin_logs: INSERT (action='toggle_slot', description='Status changed to Available')
  └─ Response: {success: true, new_status: 'Available'}

01:30:54 - Analytics page auto-refreshes
  ├─ GET /api/analytics/sessions
  ├─ Query: SELECT COUNT(*) FROM parking_history WHERE status='completed'
  ├─ Result: total_sessions = 1
  ├─ Query: SELECT AVG(duration_hours) FROM parking_history WHERE status='completed'
  ├─ Result: average_duration = 0.0048 hours
  └─ Display: "1 Total Sessions", "0h 0m Avg Duration"

01:31:00 - User clicks "Print Analytics Report"
  ├─ GET /api/get_history
  ├─ Query: SELECT * FROM parking_history ORDER BY history_id DESC LIMIT 100
  ├─ Result: Returns 5 records including the completed session
  ├─ Generate HTML report with history table
  ├─ Open print window
  └─ User prints to PDF
```

---

## 7. Data Validation & Error Handling

### Validation Points

```
1. Slot Toggle
   ├─ Verify slot_id exists in parking_slots
   ├─ Verify slot_status is valid (Available/Occupied/Maintenance)
   └─ Return 404 if slot not found

2. Parking History Creation
   ├─ Verify slot_id is valid
   ├─ Verify check_in_time is not null
   ├─ Verify status is valid (active/completed/cancelled)
   └─ Verify foreign key constraint

3. Duration Calculation
   ├─ Verify check_in_time and check_out_time are valid timestamps
   ├─ Handle timezone differences
   ├─ Return 0 if calculation fails
   └─ Store as numeric(10,2)

4. Analytics Queries
   ├─ Handle null values with COALESCE
   ├─ Use COUNT(*) for aggregations
   ├─ Use indexes for performance
   └─ Return 0 if no records found
```

---

## 8. Performance Optimization

### Database Indexes

```
idx_parking_history_slot
  └─ ON parking_history(slot_id)
  └─ Used by: toggle_slot, analytics queries

idx_parking_history_vehicle
  └─ ON parking_history(vehicle_reg_number)
  └─ Used by: vehicle lookup queries

idx_parking_history_checkin
  └─ ON parking_history(check_in_time)
  └─ Used by: hourly statistics, date range queries

idx_parking_slots_status
  └─ ON parking_slots(slot_status)
  └─ Used by: summary queries

idx_parking_slots_floor
  └─ ON parking_slots(location_floor)
  └─ Used by: floor-based queries
```

### Query Optimization

```
1. Aggregation Queries
   ├─ Use COUNT(*) instead of SELECT *
   ├─ Use SUM() for conditional counts
   ├─ Use AVG() for averages
   └─ Use indexes on WHERE clauses

2. History Queries
   ├─ Limit results to 100 records
   ├─ Order by history_id DESC for latest first
   ├─ Use index on slot_id for lookups
   └─ Cache results in frontend

3. Real-Time Updates
   ├─ 10-second refresh interval (not too frequent)
   ├─ Parallel API calls (not sequential)
   ├─ Frontend caching of data
   └─ Minimal database load
```

---

## 9. Troubleshooting Data Flow

### Issue: Parking history not created

```
Check:
1. Is toggle_slot() being called?
   └─ Check browser network tab for POST /api/toggle_slot

2. Is database connection working?
   └─ Check Flask logs for connection errors

3. Is parking_history table created?
   └─ Check Supabase: SELECT * FROM parking_history;

4. Is INSERT query executing?
   └─ Check Supabase query logs

5. Is foreign key constraint satisfied?
   └─ Verify slot_id exists in parking_slots
```

### Issue: Analytics showing wrong data

```
Check:
1. Are API endpoints returning data?
   └─ curl http://localhost:5000/api/analytics/sessions

2. Is data in parking_history table?
   └─ SELECT COUNT(*) FROM parking_history;

3. Are queries filtering correctly?
   └─ Check WHERE clauses in API endpoints

4. Is frontend parsing JSON correctly?
   └─ Check browser console for errors

5. Is real-time refresh working?
   └─ Check setInterval in browser console
```

---

## Summary

The parking history system follows a complete data flow:

1. **User Action** → Slot toggle
2. **Backend Processing** → Update databases
3. **Data Storage** → parking_slots + parking_history
4. **Analytics Collection** → Aggregate queries
5. **Frontend Display** → Real-time charts and cards
6. **Report Generation** → Professional PDF

All components work together seamlessly to provide real-time parking analytics and reporting.

---

*Document Version: 1.0*  
*Last Updated: May 2, 2026*
