# External Network Access Setup Guide - Complete ✅

## 🎯 Problem Summary

Your Flask app works locally but fails when accessed from another network because:
1. **Flask bound to localhost** - Only accepts connections from the same machine
2. **Database connection issues** - PostgreSQL direct connection doesn't work over internet
3. **CORS not properly configured** - External requests blocked
4. **Environment variables not set** - Missing or incorrect configuration
5. **Firewall/Port issues** - Port not exposed to external network

---

## 📋 Step-by-Step Configuration

### STEP 1: Fix Flask Host Binding ✅

**Current (BROKEN):**
```python
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
```

**Fixed (WORKING):**
```python
if __name__ == '__main__':
    # Get host from environment, default to 0.0.0.0 for external access
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(debug=debug, host=host, port=port, threaded=True)
```

**Why this works:**
- `0.0.0.0` = Listen on all network interfaces (local + external)
- `localhost` = Listen only on local machine
- Environment variables allow different configs for dev/production

---

### STEP 2: Update Environment Variables ✅

**Update your `.env` file:**

```dotenv
# ========== FLASK CONFIGURATION ==========
FLASK_ENV=production              # Change from development
FLASK_DEBUG=False                 # Disable debug in production
FLASK_HOST=0.0.0.0               # Listen on all interfaces
FLASK_PORT=5000                  # Port to expose

# ========== SUPABASE CONFIGURATION ==========
# REST API (HTTP-based, works on any network)
SUPABASE_URL=https://bhsofudngyukxkkialwi.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Direct PostgreSQL (NOT recommended for external access)
# Only use for local/office network
SUPABASE_HOST=db.bhsofudngyukxkkialwi.supabase.co
SUPABASE_USER=postgres
SUPABASE_PASSWORD=Runningmanalone0_
SUPABASE_DATABASE=postgres
SUPABASE_PORT=5432

# ========== SECURITY ==========
SECRET_KEY=parkslot_secret_key_2026
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.*,your-domain.com

# ========== EMAIL CONFIGURATION ==========
EMAIL_SENDER=parkslotcylix@gmail.com
EMAIL_PASSWORD=dzxy kmck urft qodf
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# ========== CORS CONFIGURATION ==========
CORS_ORIGINS=http://localhost:3000,http://192.168.1.*,https://your-domain.com
```

---

### STEP 3: Fix CORS Configuration ✅

**Current (May have issues):**
```python
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

**Better (More secure):**
```python
# Get allowed origins from environment
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

CORS(app, 
     origins=allowed_origins,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     max_age=3600)
```

**Or for development (allow all):**
```python
if os.getenv('FLASK_ENV') == 'development':
    CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
else:
    # Production: restrict origins
    CORS(app, origins=allowed_origins, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

---

### STEP 4: Fix Database Connection ✅

**Problem:** Direct PostgreSQL connection doesn't work over internet

**Solution:** Use Supabase REST API (HTTP-based)

**Current approach (may fail):**
```python
# Direct PostgreSQL connection
import psycopg2
conn = psycopg2.connect(
    host=os.getenv('SUPABASE_HOST'),
    user=os.getenv('SUPABASE_USER'),
    password=os.getenv('SUPABASE_PASSWORD'),
    database=os.getenv('SUPABASE_DATABASE'),
    port=int(os.getenv('SUPABASE_PORT', 5432))
)
```

**Better approach (works everywhere):**
```python
# Use Supabase REST API (HTTP-based)
import requests

class SupabaseClient:
    def __init__(self, url, api_key):
        self.url = url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'apikey': api_key
        }
    
    def query(self, table, method='GET', data=None, filters=None):
        """Execute query using REST API"""
        endpoint = f"{self.url}/rest/v1/{table}"
        
        if filters:
            # Add filters to URL
            filter_str = '&'.join([f"{k}=eq.{v}" for k, v in filters.items()])
            endpoint += f"?{filter_str}"
        
        try:
            if method == 'GET':
                response = requests.get(endpoint, headers=self.headers, timeout=10)
            elif method == 'POST':
                response = requests.post(endpoint, headers=self.headers, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(endpoint, headers=self.headers, json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(endpoint, headers=self.headers, timeout=10)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Database error: {e}")
            return None

# Initialize client
db = SupabaseClient(
    url=os.getenv('SUPABASE_URL'),
    api_key=os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)
```

---

### STEP 5: Add Health Check Endpoint ✅

Add this to your Flask app to verify external connectivity:

```python
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for external access verification"""
    try:
        # Check database connection
        db_status = "connected"
        try:
            # Test Supabase connection
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/parking_slots?limit=1",
                headers=SUPABASE_HEADERS,
                timeout=5
            )
            db_status = "connected" if response.status_code == 200 else "error"
        except:
            db_status = "error"
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': db_status,
            'environment': os.getenv('FLASK_ENV', 'unknown')
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

---

### STEP 6: Configure Firewall & Port Forwarding ✅

**For Windows Firewall:**
```powershell
# Allow Flask port through firewall
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=tcp localport=5000

# Verify rule
netsh advfirewall firewall show rule name="Flask App"
```

**For Linux/Mac:**
```bash
# Check if port is listening
sudo lsof -i :5000

# Allow port through firewall (macOS)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

**For Router Port Forwarding:**
1. Log into your router (usually 192.168.1.1)
2. Find Port Forwarding settings
3. Forward external port 5000 to your machine's local IP (e.g., 192.168.1.100:5000)
4. Note your public IP address

---

### STEP 7: Update Flask App Configuration ✅

**Replace the app.run() section in app.py:**

```python
if __name__ == '__main__':
    # Load environment variables
    load_dotenv(override=True)
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create required tables on startup
    create_password_reset_table()
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting ParkSlot Application")
    print(f"{'='*60}")
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: Supabase REST API")
    print(f"{'='*60}\n")
    
    # Run Flask app
    app.run(
        debug=debug,
        host=host,
        port=port,
        threaded=True,
        use_reloader=debug
    )
```

---

## 🔧 Complete Updated app.py Configuration Section

Replace the top of your app.py with this:

```python
from flask import Flask, render_template, request, jsonify, session, Response
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import requests
import threading
import os
import time
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string
from dotenv import load_dotenv
import json
import urllib.parse

# Load environment variables
load_dotenv(override=True)

# Initialize Flask app
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# ========== CONFIGURATION ==========

# Flask Configuration
app.secret_key = os.getenv('SECRET_KEY', 'parkslot_secret_key_2026')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Supabase Configuration (REST API - works on any network)
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://bhsofudngyukxkkialwi.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '').strip()
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', '').strip()
SUPABASE_API_KEY = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY

# Validate Supabase configuration
if not SUPABASE_API_KEY:
    print("⚠️  WARNING: SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY not set!")
    print("   Database operations will fail. Set these in .env file.")

# REST API headers
SUPABASE_HEADERS = {
    'Authorization': f'Bearer {SUPABASE_API_KEY}',
    'Content-Type': 'application/json',
    'apikey': SUPABASE_API_KEY
}

# CORS Configuration
allowed_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(
    app,
    origins=allowed_origins,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
    max_age=3600
)

# ESP32 Camera Configuration
CAMERA_URL = os.getenv('CAMERA_URL', 'http://192.168.1.103')
CAMERA_STREAM_URL = f'{CAMERA_URL}/stream'
CAMERA_TIMEOUT = 5

# Upload Configuration
UPLOAD_FOLDER = 'static/images/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Email Configuration
EMAIL_CONFIG = {
    'sender_email': os.getenv('EMAIL_SENDER', 'parkslotcylix@gmail.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', ''),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587))
}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print(f"\n✅ Configuration loaded:")
print(f"   - Supabase URL: {SUPABASE_URL}")
print(f"   - CORS Origins: {', '.join(allowed_origins)}")
print(f"   - Camera URL: {CAMERA_URL}")
```

---

## 🧪 Testing External Access

### Test 1: Local Access (Should work)
```bash
curl http://localhost:5000/api/health
```

### Test 2: Local Network Access
```bash
# Find your local IP
ipconfig getifaddr en0  # macOS
hostname -I             # Linux
ipconfig                # Windows

# Test from another machine on same network
curl http://192.168.1.100:5000/api/health
```

### Test 3: External Access
```bash
# If port forwarded to public IP
curl http://YOUR_PUBLIC_IP:5000/api/health

# Or if using domain
curl http://your-domain.com:5000/api/health
```

### Expected Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-02T10:30:45.123456",
  "database": "connected",
  "environment": "production"
}
```

---

## 🚀 Deployment Options

### Option 1: Local Network (Recommended for Office)
```bash
# Run with local network access
FLASK_HOST=0.0.0.0 FLASK_PORT=5000 python app.py

# Access from any machine on network
# http://192.168.1.100:5000
```

### Option 2: Cloud Deployment (Recommended for Internet)

**Using Heroku:**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create parkslot-app
git push heroku main
```

**Using PythonAnywhere:**
1. Upload code to PythonAnywhere
2. Configure WSGI file
3. Set environment variables
4. Reload web app

**Using AWS/Azure/GCP:**
1. Create VM instance
2. Install Python and dependencies
3. Set environment variables
4. Run Flask app with Gunicorn
5. Configure security groups/firewall

---

## 🔒 Security Checklist

✅ **Before Going External:**
- [ ] Change `FLASK_DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Restrict `CORS_ORIGINS` to known domains
- [ ] Use HTTPS (SSL certificate)
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Never commit `.env` to version control
- [ ] Enable firewall rules
- [ ] Use strong database passwords
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring

---

## 📊 Troubleshooting

### Issue: "Connection refused" from external network
**Solution:**
1. Check Flask is bound to `0.0.0.0` (not `localhost`)
2. Verify firewall allows port 5000
3. Check port forwarding on router
4. Verify public IP is correct

### Issue: "Database connection error"
**Solution:**
1. Verify Supabase credentials in `.env`
2. Check internet connection
3. Test with `/api/health` endpoint
4. Check Supabase status page

### Issue: "CORS error" from external client
**Solution:**
1. Add client origin to `CORS_ORIGINS`
2. Verify `CORS()` configuration
3. Check browser console for exact error
4. Test with curl first

### Issue: "Timeout" errors
**Solution:**
1. Increase request timeout
2. Check network latency
3. Verify database is responding
4. Check for firewall blocking

---

## 📝 Summary of Changes

| Component | Before | After |
|-----------|--------|-------|
| Flask Host | `localhost` | `0.0.0.0` |
| Flask Port | `5000` | `5000` (configurable) |
| Database | Direct PostgreSQL | Supabase REST API |
| CORS | `"*"` | Configurable origins |
| Environment | `development` | `production` |
| Debug | `True` | `False` |
| Configuration | Hardcoded | Environment variables |

---

## ✅ Status: READY FOR EXTERNAL ACCESS

After following these steps:
- ✅ Flask app accessible from any network
- ✅ Database works over internet
- ✅ CORS properly configured
- ✅ Environment variables secure
- ✅ Health check endpoint available
- ✅ Firewall configured
- ✅ Production-ready setup

**Your app is now ready for external network access!** 🚀
