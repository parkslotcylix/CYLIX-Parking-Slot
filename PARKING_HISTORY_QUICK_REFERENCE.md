# Parking History System - Quick Reference Guide

## Quick Start

### 1. Start the Application
```bash
python app.py
```
Then visit: `http://localhost:5000`

### 2. View Parking Slots
```
http://localhost:5000/parking
```
Click any slot to toggle between Available/Occupied

### 3. View Analytics
```
http://localhost:5000/analytics
```
See real-time parking statistics and charts

### 4. Generate Report
Click "📄 Print Analytics Report" button on analytics page

---

## Database Queries

### View All Parking History
```sql
SELECT * FROM parking_history 
ORDER BY history_id DESC 
LIMIT 20;
```

### View Completed Sessions
```sql
SELECT * FROM parking_history 
WHERE status = 'completed' 
ORDER BY history_id DESC 
LIMIT 10;
```

### View Active Sessions
```sql
SELECT * FROM parking_history 
WHERE status = 'active' 
ORDER BY history_id DESC;
```

### Get Parking Statistics
```sql
SELECT 
  COUNT(*) as total_sessions,
  SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
  AVG(duration_hours) as avg_duration
FROM parking_history;
```

### Get Today's Parking Activity
```sql
SELECT * FROM parking_history 
WHERE DATE(check_in_time) = TODAY()
ORDER BY check_in_time DESC;
```

### Get Parking by Slot
```sql
SELECT * FROM parking_history 
WHERE slot_id = 1 
ORDER BY history_id DESC 
LIMIT 10;
```

### Calculate Total Parking Revenue
```sql
SELECT 
  SUM(parking_fee) as total_revenue,
  COUNT(*) as total_sessions,
  AVG(parking_fee) as avg_fee
FROM parking_history 
WHERE status = 'completed' AND parking_fee IS NOT NULL;
```

### Get Peak Hours
```sql
SELECT 
  EXTRACT(HOUR FROM check_in_time) as hour,
  COUNT(*) as sessions
FROM parking_history
WHERE DATE(check_in_time) = TODAY()
GROUP BY EXTRACT(HOUR FROM check_in_time)
ORDER BY sessions DESC;
```

---

## API Endpoints

### Get Parking Summary
```
GET /api/get_summary
```
**Response:**
```json
{
  "success": true,
  "summary": {
    "total": 3,
    "available": 0,
    "occupied": 3,
    "occupancy_percent": 100
  }
}
```

### Get Parking History
```
GET /api/get_history
```
**Response:**
```json
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
    }
  ]
}
```

### Toggle Slot
```
POST /api/toggle_slot
Content-Type: application/json

{
  "slot_id": 1
}
```
**Response:**
```json
{
  "success": true,
  "new_status": "Occupied",
  "timestamp": "2026-05-02 01:30:39"
}
```

### Get Analytics Sessions
```
GET /api/analytics/sessions
```
**Response:**
```json
{
  "success": true,
  "total_sessions": 2,
  "active_sessions": 3,
  "average_duration": 0.0
}
```

### Get Hourly Statistics
```
GET /api/analytics/hourly
```
**Response:**
```json
{
  "success": true,
  "hourly_stats": [0, 0, 0, ..., 2, 1, 0, ...]
}
```

---

## Testing Commands

### Test API with curl
```bash
# Get summary
curl http://localhost:5000/api/get_summary

# Get history
curl http://localhost:5000/api/get_history

# Get analytics
curl http://localhost:5000/api/analytics/sessions

# Toggle slot (requires POST)
curl -X POST http://localhost:5000/api/toggle_slot \
  -H "Content-Type: application/json" \
  -d '{"slot_id": 1}'
```

### Run Verification Script
```bash
python verify_system.py
```

---

## Common Issues & Solutions

### Issue: "Database connection failed"
**Solution:**
1. Check `.env` file has correct database credentials
2. Verify Supabase is running
3. Test connection: `psql -h [host] -U [user] -d [database]`

### Issue: "Slot not found"
**Solution:**
1. Verify slot_id exists in parking_slots table
2. Check slot_id is numeric
3. Query: `SELECT * FROM parking_slots WHERE slot_id = 1;`

### Issue: "No parking history records"
**Solution:**
1. Verify parking_history table exists
2. Toggle a slot to create a record
3. Check: `SELECT COUNT(*) FROM parking_history;`

### Issue: "Analytics page not loading"
**Solution:**
1. Check browser console (F12) for errors
2. Verify API endpoints are responding
3. Check user is logged in (sessionStorage)
4. Clear browser cache and reload

### Issue: "Print report not working"
**Solution:**
1. Check popup blocker is disabled
2. Verify `/api/get_history` is working
3. Check browser console for errors
4. Try different browser

### Issue: "Slow performance"
**Solution:**
1. Check database indexes exist
2. Archive old parking_history records
3. Monitor database query times
4. Check network latency

---

## Maintenance Tasks

### Archive Old Records (Monthly)
```sql
-- Move records older than 90 days to archive table
INSERT INTO parking_history_archive
SELECT * FROM parking_history 
WHERE created_at < NOW() - INTERVAL '90 days';

-- Delete archived records
DELETE FROM parking_history 
WHERE created_at < NOW() - INTERVAL '90 days';
```

### Rebuild Indexes (Quarterly)
```sql
REINDEX INDEX idx_parking_history_slot;
REINDEX INDEX idx_parking_history_vehicle;
REINDEX INDEX idx_parking_history_checkin;
REINDEX INDEX idx_parking_slots_status;
REINDEX INDEX idx_parking_slots_floor;
```

### Verify Data Integrity
```sql
-- Check for orphaned records
SELECT * FROM parking_history 
WHERE slot_id NOT IN (SELECT slot_id FROM parking_slots);

-- Check for invalid status values
SELECT DISTINCT status FROM parking_history;

-- Check for missing check_out times on completed sessions
SELECT * FROM parking_history 
WHERE status = 'completed' AND check_out_time IS NULL;
```

---

## Performance Metrics

### Expected Response Times
- API endpoints: < 100ms
- Analytics page load: < 500ms
- Print report generation: < 1s
- Database queries: < 50ms (with indexes)

### Database Size Estimates
- 1,000 parking sessions: ~100 KB
- 10,000 parking sessions: ~1 MB
- 100,000 parking sessions: ~10 MB
- 1,000,000 parking sessions: ~100 MB

### Recommended Archival
- Archive records older than 90 days
- Keep last 12 months in active table
- Archive to separate table for historical analysis

---

## File Locations

### Backend
- `app.py` - Main Flask application
- `config/db.php` - Database configuration
- `.env` - Environment variables

### Frontend
- `templates/analytics.html` - Analytics page
- `templates/parking.html` - Parking slots page
- `static/images/` - Images and logos

### Documentation
- `PARKING_HISTORY_FIXED.md` - Implementation details
- `ANALYTICS_PARKING_HISTORY_INTEGRATION.md` - Integration guide
- `SYSTEM_VERIFICATION_REPORT.md` - Verification results
- `PARKING_HISTORY_DATA_FLOW.md` - Data flow diagram

### Testing
- `verify_system.py` - System verification script
- `test_parking_history.py` - Parking history tests
- `verify_parking_history.py` - Database verification

---

## Key Features

✅ **Automatic History Tracking**
- Every slot toggle creates/updates parking_history record
- Timestamps automatically recorded
- Duration calculated automatically

✅ **Real-Time Analytics**
- Live parking statistics
- 24-hour occupancy chart
- Peak hours analysis
- Auto-refresh every 10 seconds

✅ **Professional Reports**
- PDF-ready format
- Executive summary
- Key metrics
- Parking history table
- Print-friendly design

✅ **Performance Optimized**
- Database indexes on all key columns
- Efficient queries with aggregation
- Parallel API calls
- Minimal database load

✅ **Audit Trail**
- All actions logged to admin_logs
- Complete history of slot changes
- Timestamps for all events
- User tracking capability

---

## Next Steps

1. **Monitor System**
   - Watch parking_history records being created
   - Check analytics page for accuracy
   - Monitor performance metrics

2. **Test Features**
   - Toggle slots and verify history
   - Generate reports and verify content
   - Test analytics calculations

3. **Optimize**
   - Archive old records
   - Monitor database size
   - Tune query performance

4. **Extend**
   - Add vehicle registration tracking
   - Implement parking fees
   - Add user notifications
   - Create mobile app

---

## Support

For issues or questions:
1. Check this quick reference guide
2. Review SYSTEM_VERIFICATION_REPORT.md
3. Check PARKING_HISTORY_DATA_FLOW.md
4. Review Flask logs: `python app.py`
5. Check browser console: F12 → Console tab

---

*Quick Reference Version: 1.0*  
*Last Updated: May 2, 2026*
