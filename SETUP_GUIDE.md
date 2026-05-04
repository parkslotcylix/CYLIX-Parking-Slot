# Smart Parking Slot System - Setup Guide

## Project Structure

```
ParkSlot/
├── config/
│   └── db.php              # Database connection
├── api/
│   └── parking.php         # API endpoints for parking operations
├── templates/
│   ├── home.html           # Home page with dashboard
│   ├── analytics.html      # Analytics and reporting page
│   ├── parking.html        # Parking slots management
│   └── account.html        # Admin account management
├── static/
│   └── images/
│       ├── green.png       # Slot 1 car image
│       ├── orange.png      # Slot 2 car image
│       └── red.png         # Slot 3 car image
└── sample/
    └── parking_slot.html   # Original single-file version
```

## Database Setup

### 1. Create Database
```sql
CREATE DATABASE IF NOT EXISTS parkingslot;
```

### 2. Import SQL Schema
- Open phpMyAdmin or MySQL client
- Select the `parkingslot` database
- Import the provided SQL file (parking_slot_database.sql)

### 3. Verify Tables
The following tables will be created:
- `admin` - Admin user credentials
- `admin_logs` - Action logs
- `parking_history` - Parking session history
- `parking_rates` - Parking pricing
- `parking_slots` - Slot information and status
- `system_settings` - System configuration

## Configuration

### Update Database Connection
Edit `config/db.php` with your database credentials:

```php
define('DB_HOST', 'localhost');      // Your host
define('DB_USER', 'root');           // Your username
define('DB_PASS', '');               // Your password
define('DB_NAME', 'parkingslot');    // Database name
```

## Running the Application

### Local Development (Using PHP Built-in Server)

1. Navigate to project root:
```bash
cd ParkSlot
```

2. Start PHP server:
```bash
php -S localhost:8000
```

3. Access templates:
- Home: http://localhost:8000/templates/home.html
- Analytics: http://localhost:8000/templates/analytics.html
- Parking: http://localhost:8000/templates/parking.html
- Account: http://localhost:8000/templates/account.html

## API Endpoints

All API requests go to: `../api/parking.php?action=ACTION`

### Available Actions

#### 1. Get All Parking Slots
```
GET /api/parking.php?action=get_slots
```
Returns: Array of all parking slots with current status

#### 2. Toggle Slot Status
```
POST /api/parking.php?action=toggle_slot
Body: { "slot_id": 1 }
```
Toggles slot between Available and Occupied

#### 3. Get Parking Summary
```
GET /api/parking.php?action=get_summary
```
Returns: Available, Occupied, Total slots, Occupancy percentage

#### 4. Reset All Slots
```
POST /api/parking.php?action=reset_slots
```
Sets all slots to Available status

#### 5. Get Parking History
```
GET /api/parking.php?action=get_history
```
Returns: Recent parking session history

#### 6. Get Parking Rates
```
GET /api/parking.php?action=get_rates
```
Returns: Active parking rates

#### 7. Get Admin Information
```
GET /api/parking.php?action=get_admin
```
Returns: Admin account details

## Features

### Home Page
- Dashboard showing real-time parking status
- Live monitoring badge
- Quick access to other sections
- Statistics cards (available, occupied, occupancy %)

### Parking Page
- Visual representation of parking slots
- Click to toggle slot status
- Time stamps for when slots became occupied
- Camera feed simulation
- Parking statistics footer
- Reset all slots button

### Analytics Page
- Occupancy rate chart (24-hour)
- Peak hours analysis
- Parking statistics
- Available parking slots display

### Account Page
- Admin information display
- Access level information
- Personal controls
- Report and logout buttons

## Data Synchronization

- **Parking Page**: Refreshes every 5 seconds
- **Home Dashboard**: Refreshes every 5 seconds
- **Analytics**: Refreshes every 10 seconds

All pages automatically sync with database data.

## Default Admin Account

```
Username: admin@smartparking.com
Password: admin123
Access Level: Super Admin
```

## Troubleshooting

### Database Connection Error
- Verify MySQL/MariaDB is running
- Check database credentials in `config/db.php`
- Ensure database user has proper permissions

### API Not Responding
- Check PHP error logs
- Verify `api/parking.php` path is correct from templates
- Confirm database tables exist

### Images Not Displaying
- Verify image files exist in `static/images/`
- Check image file names (green.png, orange.png, red.png)
- Verify relative paths in HTML

## Security Notes

⚠️ **Development Only** - This is a development setup. For production:
- Use environment variables for database credentials
- Implement proper authentication
- Add input validation and sanitization
- Use prepared statements for all queries
- Enable HTTPS
- Implement rate limiting on API endpoints
- Add CORS restrictions

## Support

For issues or questions, refer to the database schema documentation or modify the API endpoints in `api/parking.php`.
