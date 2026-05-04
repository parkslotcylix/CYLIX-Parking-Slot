# Flask Setup Guide - Smart Parking Slot System

## ✅ Conversion Complete!

Your project has been successfully converted from **PHP to Flask (Python)**. The system now uses:
- **Backend**: Flask (Python web framework)
- **Database**: MySQL/MariaDB (unchanged)
- **Frontend**: HTML5, CSS3, JavaScript (updated API calls)

---

## 📋 Installation Steps

### 1. **Install Python Dependencies**

```bash
# Navigate to project folder
cd c:\Users\kydel\Downloads\ParkSlot

# Install required packages
pip install -r requirements.txt
```

**Required Packages:**
- Flask 2.3.3
- Flask-CORS 4.0.0
- Flask-MySQLdb 1.1.0
- MySQLdb 1.2.5
- Werkzeug 2.3.7

### 2. **Verify Database Configuration**

The Flask app reads from `app.py` which has these default settings:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'parkingslot'
```

✅ **These match your existing setup** - no changes needed!

### 3. **Ensure MySQL is Running**

```bash
# Make sure your MySQL/MariaDB server is running
# You can verify with:
# - MySQL Command Line: mysql -u root -p
# - Or check Services on Windows (MariaDB should be running)
```

---

## 🚀 Running the Flask Server

### Start Flask Development Server:

```bash
python app.py
```

You should see output like:
```
* Running on http://localhost:5000
* Debug mode: on
```

### Access the Application:

- **URL**: http://localhost:5000
- **Login Page**: http://localhost:5000 (automatically shown)
- **Home Page**: http://localhost:5000/home

---

## 🔐 Login Credentials

Use your existing MySQL admin credentials:
- **Email**: `admin@smartparking.com`
- **Password**: `admin123`

---

## 📂 Project Structure

```
ParkSlot/
├── app.py                 ← MAIN FLASK APPLICATION (Run this!)
├── requirements.txt       ← Python dependencies
├── templates/             ← HTML files (unchanged)
│   ├── login.html
│   ├── home.html
│   ├── parking.html
│   ├── analytics.html
│   └── account.html
├── static/                ← CSS, images, JavaScript
│   ├── images/
│   │   ├── green.png
│   │   ├── orange.png
│   │   ├── red.png
│   │   └── UI DESIGN-RTS.png
│   └── styles.css
├── config/
│   └── db.php            ← (Legacy PHP - no longer used)
└── api/
    └── parking.php       ← (Legacy PHP - no longer used)
```

---

## 🔄 API Endpoints (Now Flask Routes)

All API calls have been updated in the HTML files:

| Action | Old PHP | New Flask |
|--------|---------|-----------|
| Login | `?action=login` | `POST /api/login` |
| Get Slots | `?action=get_slots` | `GET /api/get_slots` |
| Toggle Slot | `?action=toggle_slot` | `POST /api/toggle_slot` |
| Get Summary | `?action=get_summary` | `GET /api/get_summary` |
| Reset Slots | `?action=reset_slots` | `POST /api/reset_slots` |
| Get Admin | `?action=get_admin` | `GET /api/get_admin` |
| Get History | `?action=get_history` | `GET /api/get_history` |
| Get Rates | `?action=get_rates` | `GET /api/get_rates` |
| Health Check | `?action=health` | `GET /api/health` |

---

## ⚙️ Key Changes Made

### 1. **Database Connection**
- **Before**: PHP `config/db.php`
- **After**: Python `app.py` with Flask-MySQLdb

### 2. **API Endpoints**
- **Before**: Single `parking.php` with action parameters
- **After**: Dedicated Flask routes (`@app.route()`)

### 3. **Session Management**
- **Before**: PHP `sessionStorage` + file-based sessions
- **After**: JavaScript `sessionStorage` (same) + Flask `session`

### 4. **HTML API Calls**
- All fetch URLs updated from `../api/parking.php?action=X` to `/api/X`
- Navigation links updated from `home.html` to `/home`
- Logout redirects changed to `/` (root)

### 5. **CORS Support**
- Added Flask-CORS for cross-origin requests
- Handles OPTIONS preflight requests automatically

---

## 🧪 Testing the System

### 1. **Test API Connection**
Open browser console (F12) when on login page - you should see:
```
✅ API is accessible: {success: true, message: "API is running", ...}
```

### 2. **Test Login**
- Enter: `admin@smartparking.com` / `admin123`
- Click "Login"
- Should redirect to `/home` dashboard

### 3. **Test Features**
- **Home**: Shows parking slot counts
- **Parking**: Click slots to toggle status
- **Analytics**: Displays occupancy charts
- **Account**: Shows admin information

---

## 🐛 Troubleshooting

### **Error: "Failed to fetch"**
```
✓ Check if Flask server is running: python app.py
✓ Verify MySQL is running
✓ Check browser console for specific error
```

### **Error: "Connection refused on port 5000"**
```
✓ Flask server not running - run: python app.py
✓ Port 5000 in use - change in app.py: app.run(port=5001)
```

### **Error: "Database connection failed"**
```
✓ Check MySQL credentials in app.py
✓ Ensure database 'parkingslot' exists
✓ Run: mysql -u root -p parkingslot
```

### **Error: "Table not found"**
```
✓ Verify all tables exist: admin, parking_slots, etc.
✓ Import SQL schema if needed
```

---

## 📝 Configuration Options

### Change Port Number:
Edit `app.py` last line:
```python
app.run(debug=True, host='localhost', port=5001)  # Change 5000 to another port
```

### Enable Debug Mode:
```python
app.run(debug=False, host='localhost', port=5000)  # Set debug=False for production
```

### Allow Remote Connections:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Access from other machines
```

---

## 🔒 Security Notes

1. **Change Secret Key**: Update `app.secret_key` in `app.py` for production
2. **Password Hashing**: Currently plain text - implement `werkzeug.security` for production
3. **CORS**: Currently allows all origins (`*`) - restrict in production
4. **Database**: Use environment variables for credentials

---

## 📚 Flask Structure Explanation

```python
# app.py main components:

1. Configuration
   - MYSQL credentials
   - Secret key for sessions
   - Flask app initialization

2. Database Connection
   - Flask-MySQLdb setup
   - DictCursor for dict-like results

3. Routes
   - /api/login (POST) - Handles authentication
   - /api/get_slots (GET) - Returns parking slots
   - /api/toggle_slot (POST) - Changes slot status
   - /api/get_summary (GET) - Summary statistics
   - /api/reset_slots (POST) - Resets all slots
   - /api/get_admin (GET) - Admin information
   - /api/health (GET) - API health check
   - / (GET) - Serves login page
   - /home, /parking, /analytics, /account - Serve templates

4. Error Handling
   - Try-catch blocks for all routes
   - JSON error responses
   - HTTP status codes
```

---

## ✨ You're All Set!

Your Smart Parking Slot system is now running on **Flask + Python** with full database integration!

### Quick Start:
```bash
cd c:\Users\kydel\Downloads\ParkSlot
python app.py
```

Then visit: http://localhost:5000

**Enjoy! 🎉**
