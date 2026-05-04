# ParkSlot System - Quick Start Guide

## Prerequisites
- Python 3.8+
- PostgreSQL (Supabase)
- Flask and dependencies installed

## Installation

### 1. Install Dependencies
```bash
pip install flask flask-cors psycopg2-binary python-dotenv requests
```

### 2. Environment Setup
Ensure `.env` file contains:
```
SUPABASE_HOST=db.bhsofudngyukxkkialwi.supabase.co
SUPABASE_USER=postgres
SUPABASE_PASSWORD=Runningmanalone0_
SUPABASE_DATABASE=postgres
SUPABASE_PORT=5432
```

### 3. Database Setup
The system automatically creates required tables on startup. No manual setup needed.

---

## Running the System

### Start Flask Server
```bash
python app.py
```

Expected output:
```
✅ Password reset tokens table created
 * Running on http://localhost:5000
 * Debug mode: on
```

### Access the Application
- **Home**: http://localhost:5000/home
- **Parking**: http://localhost:5000/parking
- **Analytics**: http://localhost:5000/analytics
- **Account**: http://localhost:5000/account

---

## Testing

### Run Comprehensive Tests
```bash
python comprehensive_test.py
```

This tests:
- API connectivity
- All analytics endpoints
- Database connection
- All pages
- Slot toggle functionality

### Manual Testing

#### 1. Test Parking Page
1. Go to http://localhost:5000/parking
2. Click on a slot to toggle status
3. Verify status changes in database
4. Check parking history is created

#### 2. Test Analytics Page
1. Go to http://localhost:5000/analytics
2. Verify cards display correctly:
   - Total Sessions Completed
   - Avg. Parking Duration
   - Available Parking Slots
3. Test date filters:
   - Today
   - 7 Days
   - 1 Month
   - Custom Range
4. Verify peak hours display
5. Click "Print Report" to generate PDF

#### 3. Test Print Report
1. Click "Print Report" button
2. New window opens with formatted report
3. Print dialog appears automatically
4. Report includes:
   - Key metrics
   - Parking history table
   - Date and time
   - Professional formatting

---

## API Endpoints

### Parking Management
- `GET /api/get_slots` - Get all parking slots
- `POST /api/toggle_slot` - Toggle slot status
- `POST /api/reset_slots` - Reset all slots
- `GET /api/get_summary` - Get parking summary

### Parking History
- `GET /api/get_history` - Get parking history records

### Analytics
- `GET /api/analytics/sessions` - Get session statistics
- `GET /api/analytics/hourly` - Get hourly occupancy data
- `GET /api/analytics/revenue` - Get revenue data

### Admin
- `POST /api/login` - Admin login
- `POST /api/change_password` - Change password
- `POST /api/forgot-password` - Request password reset
- `GET /api/get_admin` - Get admin info
- `POST /api/update_admin_info` - Update admin info

---

## Database Schema

### parking_slots
```sql
- slot_id (PRIMARY KEY)
- slot_status (Available/Occupied)
- check_in_time
- check_out_time
- updated_at
```

### parking_history
```sql
- history_id (PRIMARY KEY)
- slot_id (FOREIGN KEY)
- check_in_time
- check_out_time
- duration_hours
- status (active/completed)
- created_at
```

### admin
```sql
- admin_id (PRIMARY KEY)
- admin_name
- admin_email
- admin_password
- access_level
```

### admin_logs
```sql
- log_id (PRIMARY KEY)
- admin_id
- action
- slot_id
- description
- created_at
```

---

## Troubleshooting

### Connection Refused Error
**Problem**: "No connection could be made because the target machine actively refused it"
**Solution**: 
1. Ensure Flask server is running: `python app.py`
2. Check port 5000 is not in use
3. Verify database connection in `.env`

### Database Connection Error
**Problem**: "Database connection failed"
**Solution**:
1. Verify `.env` file has correct credentials
2. Check internet connection to Supabase
3. Verify database is accessible

### Template Not Found Error
**Problem**: "TemplateNotFound: analytics.html"
**Solution**:
1. Ensure `templates/` folder exists
2. Verify `analytics.html` is in `templates/` folder
3. Restart Flask server

### Syntax Errors in Analytics
**Problem**: "Uncaught SyntaxError" in browser console
**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh page (Ctrl+Shift+R)
3. Check browser console for specific error

### Print Report Not Working
**Problem**: Print dialog doesn't appear
**Solution**:
1. Check browser console for errors
2. Verify `/api/get_history` endpoint is working
3. Try in different browser
4. Disable pop-up blockers

---

## Performance Tips

### Optimize Analytics Loading
- Use date filters to limit data range
- Peak hours are calculated from hourly data
- History is limited to last 100 records

### Database Optimization
- Indexes are created on frequently queried columns
- Queries use PostgreSQL-compatible syntax
- Connection pooling is handled by psycopg2

### Frontend Optimization
- Charts are rendered using Chart.js
- Auto-refresh interval: 10 seconds
- Lazy loading for history records

---

## Security Notes

⚠️ **Important**: This is a development setup. For production:
1. Use environment variables for all secrets
2. Implement proper password hashing (bcrypt)
3. Add HTTPS/SSL certificates
4. Implement rate limiting
5. Add CSRF protection
6. Validate all user inputs
7. Use prepared statements (already implemented)

---

## Support

For issues or questions:
1. Check the error message in browser console
2. Review Flask server logs
3. Check database connection
4. Verify all files are in correct locations
5. Ensure all dependencies are installed

---

## System Status

✅ All systems operational
✅ Database connected
✅ Analytics working
✅ Parking management functional
✅ Print reports generating
✅ Real-time updates active

**Ready for use!**
