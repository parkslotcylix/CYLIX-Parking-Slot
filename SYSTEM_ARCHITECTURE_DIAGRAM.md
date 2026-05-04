# Parking History System - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PARKING HISTORY SYSTEM                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      USER INTERFACE                          │  │
│  │                                                              │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                │  │
│  │  │  Parking Page    │  │  Analytics Page  │                │  │
│  │  │  /parking        │  │  /analytics      │                │  │
│  │  │                  │  │                  │                │  │
│  │  │ - Click slots    │  │ - View stats     │                │  │
│  │  │ - Toggle status  │  │ - View charts    │                │  │
│  │  │ - See updates    │  │ - Print report   │                │  │
│  │  └────────┬─────────┘  └────────┬─────────┘                │  │
│  │           │                     │                          │  │
│  └───────────┼─────────────────────┼──────────────────────────┘  │
│              │                     │                             │
│  ┌───────────▼─────────────────────▼──────────────────────────┐  │
│  │                    API LAYER (Flask)                       │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ POST /api/toggle_slot                               │ │  │
│  │  │ - Toggle slot status                                │ │  │
│  │  │ - Create/update parking_history                     │ │  │
│  │  │ - Log to admin_logs                                 │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ GET /api/analytics/sessions                          │ │  │
│  │  │ - Count completed sessions                           │ │  │
│  │  │ - Count active sessions                              │ │  │
│  │  │ - Calculate average duration                         │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ GET /api/analytics/hourly                            │ │  │
│  │  │ - Get hourly occupancy data                          │ │  │
│  │  │ - Calculate peak hours                               │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ GET /api/get_history                                 │ │  │
│  │  │ - Retrieve parking history records                   │ │  │
│  │  │ - Return last 100 records                            │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ GET /api/get_summary                                 │ │  │
│  │  │ - Get parking slot summary                           │ │  │
│  │  │ - Calculate occupancy percentage                     │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                    │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │                   DATABASE LAYER                         │  │
│  │                  (Supabase PostgreSQL)                   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ parking_slots                                    │   │  │
│  │  │ ├─ slot_id (PK)                                 │   │  │
│  │  │ ├─ slot_status (Available/Occupied)             │   │  │
│  │  │ ├─ check_in_time                                │   │  │
│  │  │ ├─ check_out_time                               │   │  │
│  │  │ └─ vehicle_reg_number                           │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ parking_history                                  │   │  │
│  │  │ ├─ history_id (PK)                              │   │  │
│  │  │ ├─ slot_id (FK)                                 │   │  │
│  │  │ ├─ check_in_time                                │   │  │
│  │  │ ├─ check_out_time                               │   │  │
│  │  │ ├─ duration_hours (calculated)                  │   │  │
│  │  │ ├─ status (active/completed/cancelled)          │   │  │
│  │  │ └─ created_at                                   │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ admin_logs                                       │   │  │
│  │  │ ├─ log_id (PK)                                  │   │  │
│  │  │ ├─ action (toggle_slot)                         │   │  │
│  │  │ ├─ slot_id                                      │   │  │
│  │  │ └─ description                                  │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  Indexes:                                               │  │
│  │  ├─ idx_parking_history_slot                           │  │
│  │  ├─ idx_parking_history_vehicle                        │  │
│  │  ├─ idx_parking_history_checkin                        │  │
│  │  ├─ idx_parking_slots_status                           │  │
│  │  └─ idx_parking_slots_floor                            │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Slot Toggle Flow

```
USER CLICKS SLOT
    │
    ▼
JavaScript: POST /api/toggle_slot {slot_id: 1}
    │
    ▼
Flask Backend: toggle_slot()
    │
    ├─ Get current slot status
    │
    ├─ IF status = 'Available' THEN
    │  │
    │  ├─ UPDATE parking_slots (status='Occupied', check_in_time=NOW)
    │  │
    │  ├─ INSERT parking_history (slot_id, check_in_time, status='active')
    │  │
    │  └─ INSERT admin_logs (action='toggle_slot', description='...')
    │
    └─ ELSE (status = 'Occupied') THEN
       │
       ├─ UPDATE parking_slots (status='Available', check_out_time=NOW)
       │
       ├─ SELECT parking_history WHERE slot_id=? AND status='active'
       │
       ├─ Calculate duration_hours = (check_out - check_in) / 3600
       │
       ├─ UPDATE parking_history (status='completed', duration_hours, check_out_time)
       │
       └─ INSERT admin_logs (action='toggle_slot', description='...')
    │
    ▼
Return JSON response
    │
    ▼
Frontend updates UI
```

---

## Analytics Data Collection Flow

```
USER VISITS /analytics
    │
    ▼
Page loads templates/analytics.html
    │
    ▼
JavaScript: loadAnalytics()
    │
    ├─ GET /api/analytics/sessions
    │  │
    │  ├─ SELECT COUNT(*) FROM parking_history WHERE status='completed'
    │  ├─ SELECT COUNT(*) FROM parking_history WHERE status='active'
    │  ├─ SELECT AVG(duration_hours) FROM parking_history WHERE status='completed'
    │  │
    │  └─ Return: {total_sessions, active_sessions, average_duration}
    │
    ├─ GET /api/analytics/hourly
    │  │
    │  ├─ SELECT EXTRACT(HOUR FROM check_in_time), COUNT(*)
    │  ├─ FROM parking_history WHERE DATE(check_in_time) = TODAY()
    │  ├─ GROUP BY EXTRACT(HOUR FROM check_in_time)
    │  │
    │  └─ Return: {hourly_stats: [0, 0, ..., 2, 1, ...]}
    │
    └─ GET /api/get_summary
       │
       ├─ SELECT COUNT(*) as total, SUM(CASE WHEN status='Available'...)
       ├─ FROM parking_slots
       │
       └─ Return: {total, available, occupied, occupancy_percent}
    │
    ▼
Frontend displays data:
    ├─ Overview cards (statistics)
    ├─ Line chart (24-hour occupancy)
    └─ Peak hours chart
    │
    ▼
setInterval(loadAnalytics, 10000)
    │
    └─ Repeat every 10 seconds
```

---

## Report Generation Flow

```
USER CLICKS "Print Analytics Report"
    │
    ▼
JavaScript: printAnalyticsReport()
    │
    ├─ Collect current data from page
    │  ├─ totalSessions
    │  ├─ avgDuration
    │  ├─ slotsInfo
    │  └─ activeSessions
    │
    ├─ GET /api/get_history
    │  │
    │  ├─ SELECT * FROM parking_history
    │  ├─ ORDER BY history_id DESC
    │  ├─ LIMIT 100
    │  │
    │  └─ Return: {history: [...]}
    │
    ├─ Generate HTML report
    │  ├─ Header (logo, date, time)
    │  ├─ Executive summary
    │  ├─ Key metrics cards
    │  ├─ Parking history table (last 10 records)
    │  └─ Footer (copyright)
    │
    ├─ window.open() with HTML content
    │
    ▼
New window opens with report
    │
    ▼
User clicks print (Ctrl+P)
    │
    ▼
Browser print dialog
    │
    ▼
Save as PDF or print to printer
```

---

## Database Relationships

```
┌─────────────────────────┐
│   parking_slots         │
├─────────────────────────┤
│ slot_id (PK)            │
│ slot_number             │
│ slot_status             │
│ check_in_time           │
│ check_out_time          │
│ vehicle_reg_number      │
│ created_at              │
│ updated_at              │
└────────────┬────────────┘
             │
             │ (1:N)
             │ Foreign Key
             │
             ▼
┌─────────────────────────┐
│  parking_history        │
├─────────────────────────┤
│ history_id (PK)         │
│ slot_id (FK)            │
│ vehicle_reg_number      │
│ check_in_time           │
│ check_out_time          │
│ duration_hours          │
│ parking_fee             │
│ status                  │
│ notes                   │
│ created_at              │
└─────────────────────────┘

┌─────────────────────────┐
│   admin_logs            │
├─────────────────────────┤
│ log_id (PK)             │
│ admin_id                │
│ action                  │
│ slot_id                 │
│ description             │
│ created_at              │
└─────────────────────────┘
```

---

## API Endpoint Hierarchy

```
/api
├── /toggle_slot (POST)
│   └─ Toggle parking slot status
│
├── /get_summary (GET)
│   └─ Get parking slot summary
│
├── /get_history (GET)
│   └─ Get parking history records
│
└── /analytics
    ├── /sessions (GET)
    │   └─ Get session statistics
    │
    └── /hourly (GET)
        └─ Get hourly statistics
```

---

## Frontend Component Hierarchy

```
templates/analytics.html
├── Navigation Bar
│   ├── Logo
│   ├── Links (Home, Report, Parking, Account)
│   └── Logout
│
├── Analytics Header
│   ├── Title
│   └── Print Report Button
│
├── Overview Cards
│   ├── Total Sessions Completed
│   ├── Average Parking Duration
│   ├── Available Parking Slots
│   └── Active Sessions
│
├── Charts Section
│   ├── Occupancy Rate Chart (24h)
│   │   └── Line Chart (Chart.js)
│   │
│   └── Peak Hours Chart
│       └── Bar Chart (Chart.js)
│
└── JavaScript
    ├── loadAnalytics()
    ├── updateChart()
    ├── printAnalyticsReport()
    ├── checkAuthentication()
    └── handleLogout()
```

---

## Performance Optimization

```
┌─────────────────────────────────────────────────────────────┐
│                  PERFORMANCE OPTIMIZATION                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Database Indexes                                           │
│  ├─ idx_parking_history_slot                               │
│  │  └─ Used by: toggle_slot, analytics queries             │
│  │                                                         │
│  ├─ idx_parking_history_vehicle                            │
│  │  └─ Used by: vehicle lookup queries                     │
│  │                                                         │
│  ├─ idx_parking_history_checkin                            │
│  │  └─ Used by: hourly statistics, date range queries      │
│  │                                                         │
│  ├─ idx_parking_slots_status                               │
│  │  └─ Used by: summary queries                            │
│  │                                                         │
│  └─ idx_parking_slots_floor                                │
│     └─ Used by: floor-based queries                        │
│                                                             │
│  Query Optimization                                         │
│  ├─ Use COUNT(*) instead of SELECT *                       │
│  ├─ Use aggregation functions (SUM, AVG)                   │
│  ├─ Limit results (LIMIT 100)                              │
│  └─ Order by indexed columns                               │
│                                                             │
│  Frontend Optimization                                      │
│  ├─ Parallel API calls (not sequential)                    │
│  ├─ Frontend caching of data                               │
│  ├─ 10-second refresh interval (not too frequent)          │
│  └─ Minimal DOM updates                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
API Request
    │
    ▼
Try Block
    │
    ├─ Connect to database
    │  │
    │  └─ If fails: Return 500 "Database connection failed"
    │
    ├─ Execute query
    │  │
    │  └─ If fails: Return 500 with error message
    │
    ├─ Validate data
    │  │
    │  └─ If invalid: Return 404 or 400 with error message
    │
    └─ Return success response
    │
    ▼
Catch Block
    │
    └─ Return 500 with exception message
    │
    ▼
Frontend
    │
    ├─ Check response.success
    │  │
    │  ├─ If true: Display data
    │  │
    │  └─ If false: Display error message
    │
    └─ Log to console for debugging
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Web Server (Flask)                                │ │
│  │  - Runs on port 5000                               │ │
│  │  - Handles HTTP requests                           │ │
│  │  - Serves static files                             │ │
│  │  - Renders templates                               │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Database (Supabase PostgreSQL)                    │ │
│  │  - Stores parking_slots                            │ │
│  │  - Stores parking_history                          │ │
│  │  - Stores admin_logs                               │ │
│  │  - Maintains indexes                               │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Frontend (HTML/CSS/JavaScript)                    │ │
│  │  - Parking page (/parking)                         │ │
│  │  - Analytics page (/analytics)                     │ │
│  │  - Real-time updates                               │ │
│  │  - Report generation                               │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Monitoring & Logging

```
┌──────────────────────────────────────────────────────────┐
│              MONITORING & LOGGING SYSTEM                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Application Logs                                        │
│  ├─ Flask debug logs                                    │
│  ├─ Database connection logs                            │
│  ├─ Query execution logs                                │
│  └─ Error logs                                          │
│                                                          │
│  Database Logs                                           │
│  ├─ Query logs (Supabase)                               │
│  ├─ Connection logs                                     │
│  ├─ Error logs                                          │
│  └─ Performance metrics                                 │
│                                                          │
│  Admin Logs (In Database)                               │
│  ├─ All slot toggles                                    │
│  ├─ User actions                                        │
│  ├─ Timestamps                                          │
│  └─ Descriptions                                        │
│                                                          │
│  Browser Logs                                            │
│  ├─ Console logs                                        │
│  ├─ Network requests                                    │
│  ├─ JavaScript errors                                   │
│  └─ Performance metrics                                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## System Scalability

```
Current Capacity
├─ 3 parking slots
├─ 5 parking history records
├─ 100% occupancy
└─ 0 lag detected

Scaling Considerations
├─ Database
│  ├─ Archive records > 90 days
│  ├─ Partition by date
│  └─ Add read replicas
│
├─ API
│  ├─ Add caching layer
│  ├─ Implement rate limiting
│  └─ Load balance requests
│
└─ Frontend
   ├─ Increase refresh interval
   ├─ Implement pagination
   └─ Add lazy loading
```

---

*Architecture Diagram Version: 1.0*  
*Last Updated: May 2, 2026*
