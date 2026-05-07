from flask import Flask, render_template, request, jsonify, session, Response, send_from_directory, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta, timezone

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

# Load environment variables (only from .env if it exists locally)
try:
    load_dotenv(override=False)
except:
    pass

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Configuration - Supabase REST API (HTTP-based, works on any network)
# Hardcoded defaults (will be overridden by environment variables if set)
SUPABASE_URL = 'https://bhsofudngyukxkkialwi.supabase.co'
SUPABASE_SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJoc29mdWRuZ3l1a3hra2lhbHdpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzYxNDg4MywiZXhwIjoyMDkzMTkwODgzfQ.BcwHm7lt6fj0FD6Zd2LAzA9aGd3KLxW7mPfhhw94OGk'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJoc29mdWRuZ3l1a3hra2lhbHdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc2MTQ4ODMsImV4cCI6MjA5MzE5MDg4M30.sRrZ7PyEcJRmlxbLwZ0OfVzxKdJtcDvGmnH9EHFWjbU'

# Override with environment variables if they exist
env_url = os.getenv('SUPABASE_URL')
if env_url:
    SUPABASE_URL = env_url

env_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
if env_service_key:
    SUPABASE_SERVICE_ROLE_KEY = env_service_key.strip()

env_anon_key = os.getenv('SUPABASE_ANON_KEY')
if env_anon_key:
    SUPABASE_ANON_KEY = env_anon_key.strip()

SUPABASE_API_KEY = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY or 'invalid'

print(f"DEBUG: SUPABASE_URL = {SUPABASE_URL}")
print(f"DEBUG: SUPABASE_API_KEY set = {bool(SUPABASE_API_KEY and SUPABASE_API_KEY != 'invalid')}")

# REST API headers
SUPABASE_HEADERS = {
    'Authorization': f'Bearer {SUPABASE_API_KEY}',
    'Content-Type': 'application/json',
    'apikey': SUPABASE_API_KEY
}

# ESP32 Camera Configuration
CAMERA_URL = 'http://192.168.1.103'  # Change this to your ESP32 IP address
CAMERA_STREAM_URL = f'{CAMERA_URL}/stream'
CAMERA_TIMEOUT = 5

# Upload Configuration
UPLOAD_FOLDER = 'static/images/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Email Configuration
EMAIL_CONFIG = {
    'sender_email': os.getenv('EMAIL_SENDER', 'parkslotcylix@gmail.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', 'dzxy kmck urft qodf'),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587))
}

# Base URL for password reset links (use environment variable or request host)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = os.getenv('SECRET_KEY', 'parkslot_secret_key_2026')

# Enable CORS
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# ==================== Authentication Decorator ====================

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session or 'user_email' not in session:
            # For API routes, return JSON error
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            # For page routes, redirect to login
            return redirect(url_for('index'))
        
        # Check if account is active
        if session.get('status') != 'active':
            # Clear session if account is not active
            session.clear()
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Account is not active'}), 403
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    """Decorator to require super admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if user is logged in
        if 'user_id' not in session or 'user_email' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            return redirect(url_for('index'))
        
        # Check if account is active
        if session.get('status') != 'active':
            session.clear()
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Account is not active'}), 403
            return redirect(url_for('index'))
        
        # Check if user is super admin
        if session.get('access_level') != 'super_admin':
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Super Admin access required'}), 403
            return render_template('error.html', message='Access Denied: Super Admin privileges required'), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ==================== Supabase REST API Wrapper ====================

class SupabaseClient:
    """Wrapper for Supabase REST API calls"""
    
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
    
    def execute(self, query_dict):
        """Execute a query dict with table and filters"""
        return query_dict
    
    def fetchone(self, data):
        """Get first result from list"""
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return None
    
    def fetchall(self, data):
        """Get all results"""
        return data if isinstance(data, list) else []

class SupabaseCursor:
    """Mimics psycopg2 cursor for Supabase REST API"""
    
    def __init__(self, client):
        self.client = client
        self.last_data = None
    
    def execute(self, query, params=None):
        """Execute query using Supabase REST API"""
        try:
            # Simple SQL parser for common patterns
            query_upper = query.upper().strip()
            
            if query_upper.startswith('SELECT'):
                self._handle_select(query, params)
            elif query_upper.startswith('INSERT'):
                self._handle_insert(query, params)
            elif query_upper.startswith('UPDATE'):
                self._handle_update(query, params)
            elif query_upper.startswith('DELETE'):
                self._handle_delete(query, params)
            else:
                self.last_data = []
        except Exception as e:
            print(f"Supabase query error: {e}")
            self.last_data = []
    
    def _handle_select(self, query, params):
        """Handle SELECT queries"""
        try:
            # Extract table name
            table = self._extract_table(query)
            if not table:
                self.last_data = []
                return
            
            # Build URL
            url = f"{SUPABASE_URL}/rest/v1/{table}?select=*"
            
            # Add WHERE clause filters if present
            if 'WHERE' in query.upper():
                where_clause = query.split('WHERE')[1].split('ORDER')[0].strip()
                if '%s' in where_clause:
                    # Handle parameterized queries
                    if params:
                        for i, param in enumerate(params):
                            if isinstance(param, str):
                                param = f'"{param}"'
                            where_clause = where_clause.replace('%s', str(param), 1)
                    where_clause = where_clause.replace(' = ', 'eq.')
                    where_clause = where_clause.replace(' != ', 'neq.')
                    where_clause = where_clause.replace(' > ', 'gt.')
                    where_clause = where_clause.replace(' < ', 'lt.')
                    url += f"&{where_clause.strip()}"
            
            # Add ORDER BY if present
            if 'ORDER BY' in query.upper():
                order_match = query.split('ORDER BY')[1].strip()
                if 'DESC' in order_match.upper():
                    order_col = order_match.split('DESC')[0].strip()
                    url += f"&order={order_col}.desc"
                else:
                    order_col = order_match.split()[0].strip()
                    url += f"&order={order_col}.asc"
            
            # Add LIMIT if present
            if 'LIMIT' in query.upper():
                limit_match = query.split('LIMIT')[1].strip()
                limit_num = limit_match.split()[0].strip()
                url += f"&limit={limit_num}"
            
            response = requests.get(url, headers=SUPABASE_HEADERS, timeout=10)
            if response.status_code == 200:
                self.last_data = response.json()
            else:
                print(f"Supabase SELECT error: {response.status_code} - {response.text}")
                self.last_data = []
        except Exception as e:
            print(f"SELECT error: {e}")
            self.last_data = []
    
    def _handle_insert(self, query, params):
        """Handle INSERT queries"""
        try:
            table = self._extract_table_from_insert(query)
            if not table:
                self.last_data = []
                return
            
            # Extract column names and values
            columns = self._extract_columns_from_insert(query)
            if not columns or not params:
                self.last_data = []
                return
            
            # Build record dict
            record = {}
            for i, col in enumerate(columns):
                if i < len(params):
                    record[col] = params[i]
            
            url = f"{SUPABASE_URL}/rest/v1/{table}"
            response = requests.post(url, json=record, headers=SUPABASE_HEADERS, timeout=10)
            
            if response.status_code in [200, 201]:
                # Try to parse JSON response, but handle empty responses
                try:
                    self.last_data = response.json() if response.text else []
                except:
                    self.last_data = []
            else:
                print(f"Supabase INSERT error: {response.status_code} - {response.text}")
                self.last_data = []
        except Exception as e:
            print(f"INSERT error: {e}")
            self.last_data = []
    
    def _handle_update(self, query, params):
        """Handle UPDATE queries"""
        try:
            table = self._extract_table_from_update(query)
            if not table or not params:
                self.last_data = []
                return
            
            # Extract SET values and WHERE clause
            set_part = query.split('SET')[1].split('WHERE')[0]
            where_part = query.split('WHERE')[1]
            
            # Parse SET clause
            set_items = [s.strip() for s in set_part.split(',')]
            columns = []
            for item in set_items:
                col = item.split('=')[0].strip()
                columns.append(col)
            
            # Build record dict
            record = {}
            for i, col in enumerate(columns):
                if i < len(params) - 1:  # Last param is the WHERE value
                    record[col] = params[i]
            
            # Extract WHERE column and value
            where_col = where_part.split('=')[0].strip()
            where_value = params[-1]
            
            # Build filter
            filter_str = f'{where_col}=eq.{where_value}'
            if isinstance(where_value, str):
                filter_str = f'{where_col}=eq."{where_value}"'
            
            url = f"{SUPABASE_URL}/rest/v1/{table}?{filter_str}"
            response = requests.patch(url, json=record, headers=SUPABASE_HEADERS, timeout=10)
            
            if response.status_code in [200, 204]:
                # Try to parse JSON response, but handle empty responses
                try:
                    self.last_data = response.json() if response.text else []
                except:
                    self.last_data = []
            else:
                print(f"Supabase UPDATE error: {response.status_code} - {response.text}")
                self.last_data = []
        except Exception as e:
            print(f"UPDATE error: {e}")
            self.last_data = []
    
    def _handle_delete(self, query, params):
        """Handle DELETE queries"""
        try:
            table = self._extract_table(query)
            if not table or not params:
                self.last_data = []
                return
            
            # Extract WHERE clause
            where_col = query.split('WHERE')[1].split('=')[0].strip()
            where_value = params[0]
            
            filter_str = f'{where_col}=eq.{where_value}'
            if isinstance(where_value, str):
                filter_str = f'{where_col}=eq."{where_value}"'
            
            url = f"{SUPABASE_URL}/rest/v1/{table}?{filter_str}"
            response = requests.delete(url, headers=SUPABASE_HEADERS, timeout=10)
            
            if response.status_code in [200, 204]:
                self.last_data = []
            else:
                print(f"Supabase DELETE error: {response.status_code} - {response.text}")
                self.last_data = []
        except Exception as e:
            print(f"DELETE error: {e}")
            self.last_data = []
    
    def _extract_table(self, query):
        """Extract table name from query"""
        try:
            if 'FROM' in query.upper():
                from_idx = query.upper().index('FROM') + 4
                table_part = query[from_idx:].strip().split()[0]
                return table_part
        except:
            pass
        return None
    
    def _extract_table_from_insert(self, query):
        """Extract table name from INSERT query"""
        try:
            insert_idx = query.upper().index('INTO') + 4
            table_part = query[insert_idx:].strip().split()[0]
            return table_part
        except:
            pass
        return None
    
    def _extract_table_from_update(self, query):
        """Extract table name from UPDATE query"""
        try:
            update_idx = query.upper().index('UPDATE') + 6
            table_part = query[update_idx:].strip().split()[0]
            return table_part
        except:
            pass
        return None
    
    def _extract_columns_from_insert(self, query):
        """Extract column names from INSERT query"""
        try:
            start = query.index('(')
            end = query.index(')', start)
            cols_str = query[start+1:end]
            return [c.strip() for c in cols_str.split(',')]
        except:
            pass
        return []
    
    def fetchone(self):
        """Get first result"""
        if isinstance(self.last_data, list) and len(self.last_data) > 0:
            return self.last_data[0]
        elif isinstance(self.last_data, dict):
            return self.last_data
        return None
    
    def fetchall(self):
        """Get all results"""
        if isinstance(self.last_data, list):
            return self.last_data
        elif isinstance(self.last_data, dict):
            return [self.last_data]
        return []
    
    def close(self):
        """Close cursor"""
        pass

class SupabaseConnection:
    """Mimics psycopg2 connection"""
    
    def __init__(self):
        self.client = SupabaseClient(SUPABASE_URL, SUPABASE_HEADERS)
    
    def cursor(self, **kwargs):
        """Return a cursor"""
        return SupabaseCursor(self.client)
    
    def commit(self):
        """Commit transaction"""
        pass
    
    def close(self):
        """Close connection"""
        pass

# Connection functions
def get_db_connection():
    """Create and return a database connection (HTTP-based via Supabase REST API)"""
    try:
        return SupabaseConnection()
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_cursor(connection):
    """Get a cursor that returns results as dictionaries"""
    if connection is None:
        return None
    try:
        return connection.cursor()
    except Exception as e:
        print(f"Error creating cursor: {e}")
        return None

# Email sending function
def send_email(recipient_email, subject, html_content):
    """Send email using Gmail SMTP with timeout handling"""
    try:
        print(f"📧 Attempting to send email to: {recipient_email}")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = recipient_email
        
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        # Use timeout for SMTP connection
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=30) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to: {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication error: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Email sending error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Generate random token
def generate_reset_token(length=32):
    """Generate a random reset token"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Camera stream proxy endpoint
@app.route('/api/camera/stream')
def camera_stream():
    """Proxy the camera stream from ESP32"""
    def generate_stream():
        try:
            response = requests.get(CAMERA_STREAM_URL, stream=True, timeout=CAMERA_TIMEOUT)
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        yield chunk
            else:
                print(f"Camera returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Camera stream error: {e}")
        except Exception as e:
            print(f"Stream error: {e}")
    
    # Get headers from ESP32 response
    try:
        test_response = requests.head(CAMERA_STREAM_URL, timeout=CAMERA_TIMEOUT)
        content_type = test_response.headers.get('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
    except:
        content_type = 'multipart/x-mixed-replace; boundary=frame'
    
    return Response(
        generate_stream(),
        mimetype=content_type,
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Connection': 'keep-alive'
        }
    )

# Health check camera endpoint
@app.route('/api/camera/health')
def camera_health():
    """Check if camera is accessible"""
    try:
        response = requests.head(CAMERA_URL, timeout=CAMERA_TIMEOUT)
        return jsonify({
            'success': True,
            'camera_connected': response.status_code == 200,
            'camera_url': CAMERA_URL
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'camera_connected': False,
            'error': str(e),
            'camera_url': CAMERA_URL
        })


# Health check endpoint
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = get_db_cursor(connection)
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'API is running',
            'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def fetch_admin_by_email(email):
    """Fetch a single admin row directly from Supabase REST."""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/admin",
        headers=SUPABASE_HEADERS,
        params={
            'select': 'admin_id,admin_name,admin_email,access_level,admin_password',
            'admin_email': f'eq.{email}',
            'limit': 1
        },
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(f"Supabase admin lookup failed: {response.status_code} - {response.text}")

    rows = response.json()
    return rows[0] if rows else None

# Login endpoint
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400

        # Query admin table directly through Supabase REST so login works over any network.
        admin = fetch_admin_by_email(email)

        if admin and admin.get('admin_password') == password:
            # Check admin status
            status = admin.get('status', 'active')
            
            if status == 'inactive':
                return jsonify({
                    'success': False,
                    'error': 'Account Inactive',
                    'message': 'Your account has been deactivated. Please contact the administrator.',
                    'status': 'inactive'
                }), 403
            
            if status == 'suspended':
                return jsonify({
                    'success': False,
                    'error': 'Account Suspended',
                    'message': 'Your account has been suspended. Please contact the administrator.',
                    'status': 'suspended'
                }), 403
            
            # Store session data
            session['user_email'] = admin['admin_email']
            session['user_id'] = admin['admin_id']
            session['user_name'] = admin['admin_name']
            session['access_level'] = admin['access_level']
            session['status'] = admin.get('status', 'active')
            session['profile_picture'] = admin.get('profile_picture', '/static/images/default-profile.png')

            return jsonify({
                'success': True,
                'message': 'Login successful',
                'admin_id': admin['admin_id'],
                'admin_name': admin['admin_name'],
                'admin_email': admin['admin_email'],
                'access_level': admin['access_level'],
                'status': admin.get('status', 'active'),
                'profile_picture': admin.get('profile_picture', '/static/images/default-profile.png')
            })

        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

# Get all parking slots with current duration for occupied slots
@app.route('/api/get_slots', methods=['GET', 'OPTIONS'])
@login_required
def get_slots():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/parking_slots",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'select': '*', 'order': 'slot_id.asc'},
            timeout=10
        )
        if response.status_code == 200:
            slots = response.json()
            # Calculate current duration for occupied slots
            for slot in slots:
                if slot['slot_status'] == 'Occupied' and slot.get('check_in_time'):
                    try:
                        check_in_str = slot['check_in_time']
                        # Try ISO format first (2026-05-04T18:13:31)
                        try:
                            # Remove timezone info if present, keep naive datetime
                            check_in = datetime.fromisoformat(check_in_str.replace('Z', '+08:00'))
                            current_duration = (datetime.now(timezone.utc) - check_in).total_seconds() 
                        except Exception as iso_err:
                            # Fall back to space format (2026-05-04 18:13:31)
                            print(f"ISO parse failed: {iso_err}, trying space format")
                            check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                        
                        current_duration = (datetime.now() - check_in).total_seconds() / 3600
                        slot['current_duration_hours'] = round(current_duration, 2)
                    except Exception as e:
                        print(f"Error parsing slot duration: {e}")
                        slot['current_duration_hours'] = 0
                else:
                    slot['current_duration_hours'] = 0
            
            return jsonify({'success': True, 'slots': slots})
        else:
            return jsonify({'success': False, 'error': response.text}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Toggle slot status
@app.route('/api/toggle_slot', methods=['POST', 'OPTIONS'])
@login_required
def toggle_slot():
    try:
        data = request.get_json()
        slot_id = data.get('slot_id')
        client_timestamp = data.get('client_timestamp')

        # Get current slot
        get_resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/parking_slots",
            headers=SUPABASE_HEADERS,
            params={'select': 'slot_id,slot_status,check_in_time', 'slot_id': f'eq.{slot_id}'},
            timeout=10
        )
        if get_resp.status_code != 200 or not get_resp.json():
            return jsonify({'success': False, 'error': 'Slot not found'}), 404

        slot = get_resp.json()[0]
        current_status = slot['slot_status']

        # Parse timestamp
        try:
            client_dt = datetime.fromisoformat(client_timestamp.replace('Z', '+08:00'))
            now = client_dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        except:
            now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        if current_status == 'Available':
            new_status = 'Occupied'
            patch_data = {'slot_status': 'Occupied', 'check_in_time': now, 'updated_at': now}
        else:
            new_status = 'Available'
            patch_data = {'slot_status': 'Available', 'check_out_time': now, 'updated_at': now}

        # Update slot
        patch_resp = requests.patch(
            f"{SUPABASE_URL}/rest/v1/parking_slots",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'slot_id': f'eq.{slot_id}'},
            json=patch_data,
            timeout=10
        )
        if patch_resp.status_code not in [200, 204]:
            return jsonify({'success': False, 'error': f'Update failed: {patch_resp.text}'}), 500

        # History records
        if new_status == 'Occupied':
            requests.post(
                f"{SUPABASE_URL}/rest/v1/parking_history",
                headers=SUPABASE_HEADERS,
                json={'slot_id': slot_id, 'check_in_time': now, 'status': 'active', 'created_at': now},
                timeout=10
            )
        else:
            hist_resp = requests.get(
                f"{SUPABASE_URL}/rest/v1/parking_history",
                headers=SUPABASE_HEADERS,
                params={'select': 'history_id,check_in_time', 'slot_id': f'eq.{slot_id}',
                        'status': 'eq.active', 'order': 'history_id.desc', 'limit': 1},
                timeout=10
            )
            if hist_resp.status_code == 200 and hist_resp.json():
                history = hist_resp.json()[0]
                try:
                    check_in = datetime.strptime(history['check_in_time'], '%Y-%m-%d %H:%M:%S')
                    check_out = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
                    duration_hours = (check_out - check_in).total_seconds() / 3600
                except:
                    duration_hours = 0
                requests.patch(
                    f"{SUPABASE_URL}/rest/v1/parking_history",
                    headers=SUPABASE_HEADERS,
                    params={'history_id': f'eq.{history["history_id"]}'},
                    json={'check_out_time': now, 'status': 'completed', 'duration_hours': duration_hours},
                    timeout=10
                )

        # Log action
        requests.post(
            f"{SUPABASE_URL}/rest/v1/admin_logs",
            headers=SUPABASE_HEADERS,
            json={'admin_id': 1, 'action': 'toggle_slot', 'slot_id': slot_id,
                  'description': f'Status changed to {new_status}'},
            timeout=10
        )

        return jsonify({'success': True, 'new_status': new_status, 'timestamp': now})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    try:
        data = request.get_json()
        slot_id = data.get('slot_id')
        client_timestamp = data.get('client_timestamp')  # Get client-provided timestamp
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Get current slot status
            cursor.execute(
                "SELECT slot_status, check_in_time FROM parking_slots WHERE slot_id = %s",
                (slot_id,)
            )
            slot = cursor.fetchone()
            
            if slot:
                current_status = slot['slot_status']
                
                # Use client timestamp if provided, otherwise fall back to server time
                if client_timestamp:
                    try:
                        # Parse client timestamp (ISO format from JavaScript)
                        client_dt = datetime.fromisoformat(client_timestamp.replace('Z', '+08:00'))
                        now = client_dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        # Fallback to server time if parsing fails
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if current_status == 'Available':
                    # Transitioning to Occupied
                    new_status = 'Occupied'
                    check_in_time = now
                    
                    # 1. Update parking_slots
                    cursor.execute(
                        "UPDATE parking_slots SET slot_status = %s, check_in_time = %s, updated_at = %s WHERE slot_id = %s",
                        (new_status, check_in_time, now, slot_id)
                    )
                    
                    # 2. Create parking_history record
                    cursor.execute(
                        """INSERT INTO parking_history (slot_id, check_in_time, status, created_at) 
                           VALUES (%s, %s, %s, %s)""",
                        (slot_id, check_in_time, 'active', now)
                    )
                else:
                    # Transitioning to Available
                    new_status = 'Available'
                    check_out_time = now
                    
                    # 1. Update parking_slots
                    cursor.execute(
                        "UPDATE parking_slots SET slot_status = %s, check_out_time = %s, updated_at = %s WHERE slot_id = %s",
                        (new_status, check_out_time, now, slot_id)
                    )
                    
                    # 2. Get active history record and update it
                    cursor.execute(
                        """SELECT history_id, check_in_time FROM parking_history 
                           WHERE slot_id = %s AND status = 'active' 
                           ORDER BY history_id DESC LIMIT 1""",
                        (slot_id,)
                    )
                    history = cursor.fetchone()
                    
                    if history:
                        try:
                            check_in = datetime.strptime(history['check_in_time'], '%Y-%m-%d %H:%M:%S')
                            check_out = datetime.strptime(check_out_time, '%Y-%m-%d %H:%M:%S')
                            duration_hours = (check_out - check_in).total_seconds() / 3600
                        except:
                            duration_hours = 0
                        
                        cursor.execute(
                            """UPDATE parking_history 
                               SET check_out_time = %s, status = %s, duration_hours = %s
                               WHERE history_id = %s""",
                            (check_out_time, 'completed', duration_hours, history['history_id'])
                        )
                
                connection.commit()
                
                # Log the action
                cursor.execute(
                    "INSERT INTO admin_logs (admin_id, action, slot_id, description) VALUES (%s, %s, %s, %s)",
                    (1, 'toggle_slot', slot_id, f'Status changed to {new_status}')
                )
                connection.commit()
                cursor.close()
                
                return jsonify({
                    'success': True,
                    'new_status': new_status,
                    'timestamp': now
                })
            else:
                cursor.close()
                return jsonify({'success': False, 'error': 'Slot not found'}), 404
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get parking summary
@app.route('/api/get_summary', methods=['GET', 'OPTIONS'])
def get_summary():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            cursor.execute("SELECT COUNT(*) as available FROM parking_slots WHERE slot_status = 'Available'")
            available = cursor.fetchone()['available']
            
            cursor.execute("SELECT COUNT(*) as occupied FROM parking_slots WHERE slot_status = 'Occupied'")
            occupied = cursor.fetchone()['occupied']
            
            cursor.execute("SELECT COUNT(*) as total FROM parking_slots")
            total = cursor.fetchone()['total']
            
            cursor.close()
            
            occupancy_percent = round((occupied / total) * 100) if total > 0 else 0
            
            return jsonify({
                'success': True,
                'summary': {
                    'available': available,
                    'occupied': occupied,
                    'total': total,
                    'occupancy_percent': occupancy_percent
                }
            })
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Reset all slots
@app.route('/api/reset_slots', methods=['POST', 'OPTIONS'])
@login_required
def reset_slots():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            cursor.execute(
                "UPDATE parking_slots SET slot_status = 'Available', check_in_time = NULL, check_out_time = NULL"
            )
            connection.commit()
            
            # Log the action
            cursor.execute(
                "INSERT INTO admin_logs (admin_id, action, description) VALUES (%s, %s, %s)",
                (1, 'reset_slots', 'All slots reset to available')
            )
            connection.commit()
            cursor.close()
            
            return jsonify({'success': True, 'message': 'All slots reset'})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Update slot status from hardware (camera/Arduino) with client timestamp
@app.route('/api/update_slot_from_hardware', methods=['POST', 'OPTIONS'])
def update_slot_from_hardware():
    try:
        data = request.get_json()
        slot_id = data.get('slot_id')
        status = data.get('status')  # 0 = Available, 1 = Occupied
        client_timestamp = data.get('client_timestamp')  # Get client-provided timestamp

        if slot_id is None or status is None:
            return jsonify({'success': False, 'error': 'Missing slot_id or status'}), 400

        new_status = 'Occupied' if int(status) == 1 else 'Available'
        
        # Parse timestamp - use EXACT same logic as toggle_slot
        try:
            # Client sends ISO format with timezone info
            client_dt = datetime.fromisoformat(client_timestamp.replace('Z', '+00:00'))
            # Convert to naive datetime in client's timezone (remove timezone info)
            # This preserves the local time the client sees
            now = client_dt.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Timestamp parse error: {e}, using server time")
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 1. Get current slot status directly from Supabase
        get_resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/parking_slots",
            headers=SUPABASE_HEADERS,
            params={'select': 'slot_id,slot_status', 'slot_id': f'eq.{slot_id}'},
            timeout=10
        )
        if get_resp.status_code != 200 or not get_resp.json():
            return jsonify({'success': False, 'error': f'Slot {slot_id} not found'}), 404

        current_status = get_resp.json()[0]['slot_status']

        # 2. Only act if status actually changed
        if new_status == current_status:
            return jsonify({'success': True, 'slot_id': slot_id, 'new_status': new_status, 'changed': False, 'timestamp': now})

        if new_status == 'Occupied':
            patch_data = {'slot_status': 'Occupied', 'check_in_time': now, 'updated_at': now}
        else:
            patch_data = {'slot_status': 'Available', 'check_out_time': now, 'updated_at': now}

        # 3. Update parking_slots
        patch_resp = requests.patch(
            f"{SUPABASE_URL}/rest/v1/parking_slots",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'slot_id': f'eq.{slot_id}'},
            json=patch_data,
            timeout=10
        )
        if patch_resp.status_code not in [200, 204]:
            return jsonify({'success': False, 'error': f'Update failed: {patch_resp.text}'}), 500

        # 4. Insert/update parking_history
        if new_status == 'Occupied':
            requests.post(
                f"{SUPABASE_URL}/rest/v1/parking_history",
                headers=SUPABASE_HEADERS,
                json={'slot_id': slot_id, 'check_in_time': now, 'status': 'active', 'created_at': now},
                timeout=10
            )
        else:
            # Find and close the active history record
            hist_resp = requests.get(
                f"{SUPABASE_URL}/rest/v1/parking_history",
                headers=SUPABASE_HEADERS,
                params={'select': 'history_id,check_in_time', 'slot_id': f'eq.{slot_id}',
                        'status': 'eq.active', 'order': 'history_id.desc', 'limit': 1},
                timeout=10
            )
            if hist_resp.status_code == 200 and hist_resp.json():
                history = hist_resp.json()[0]
                try:
                    check_in = datetime.strptime(history['check_in_time'], '%Y-%m-%d %H:%M:%S')
                    check_out = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
                    duration_hours = (check_out - check_in).total_seconds() / 3600
                except:
                    duration_hours = 0
                requests.patch(
                    f"{SUPABASE_URL}/rest/v1/parking_history",
                    headers=SUPABASE_HEADERS,
                    params={'history_id': f'eq.{history["history_id"]}'},
                    json={'check_out_time': now, 'status': 'completed', 'duration_hours': duration_hours},
                    timeout=10
                )

        print(f"[Hardware] Slot {slot_id}: {current_status} → {new_status} at {now}")
        return jsonify({'success': True, 'slot_id': slot_id, 'new_status': new_status, 'timestamp': now})

    except Exception as e:
        print(f"[Hardware] Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Get parking history with calculated durations
@app.route('/api/get_history', methods=['GET', 'OPTIONS'])
@login_required
def get_history():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/parking_history",
            headers=SUPABASE_HEADERS,
            params={
                'select': '*',
                'order': 'history_id.desc',
                'limit': 100
            },
            timeout=10
        )
        
        if response.status_code == 200:
            history = response.json()
            # Recalculate durations to ensure accuracy
            for record in history:
                if record.get('check_in_time') and record.get('check_out_time'):
                    try:
                        # Parse timestamps - handle both ISO format (T separator) and space format
                        check_in_str = record['check_in_time']
                        check_out_str = record['check_out_time']
                        
                        # Try ISO format first (2026-05-04T18:13:31)
                        try:
                            # Remove timezone info if present, keep naive datetime
                            check_in = datetime.fromisoformat(check_in_str.replace('Z', '+08:00'))
                            check_out = datetime.fromisoformat(check_out_str.replace('Z', '+08:00'))
                        except Exception as iso_err:
                            # Fall back to space format (2026-05-04 18:13:31)
                            print(f"ISO parse failed: {iso_err}, trying space format")
                            check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                            check_out = datetime.strptime(check_out_str, '%Y-%m-%d %H:%M:%S')
                        
                        calculated_duration = (check_out - check_in).total_seconds() / 3600
                        record['duration_hours'] = round(calculated_duration, 2)
                        # Also calculate parking fee if needed (e.g., 5 per hour)
                        record['parking_fee'] = round(calculated_duration * 5, 2)
                    except Exception as e:
                        print(f"Error parsing duration: {e}")
                        record['duration_hours'] = 0
                        record['parking_fee'] = 0
                elif record.get('check_in_time') and record.get('status') == 'active':
                    # Currently occupied - calculate from check_in to now
                    try:
                        check_in_str = record['check_in_time']
                        # Try ISO format first
                        try:
                            # Remove timezone info if present, keep naive datetime
                            check_in_clean = check_in_str.replace('Z', '+08:00')
                            check_in = datetime.fromisoformat(check_in_clean)
                        except Exception as iso_err:
                            # Fall back to space format
                            print(f"ISO parse failed: {iso_err}, trying space format")
                            check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                        
                        current_duration = (datetime.now(timezone.utc) - check_in).total_seconds() / 3600
                        record['duration_hours'] = round(current_duration, 2)
                        record['parking_fee'] = round(current_duration * 5, 2)
                    except Exception as e:
                        print(f"Error parsing active duration: {e}")
                        record['duration_hours'] = 0
                        record['parking_fee'] = 0
            
            return jsonify({'success': True, 'history': history})
        else:
            return jsonify({'success': False, 'error': response.text}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get filtered parking history for reports with calculated durations
@app.route('/api/get_history_filtered', methods=['GET', 'OPTIONS'])
@login_required
def get_history_filtered():
    import os
    
    # Create a test file to confirm this code is running
    test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'endpoint_called.txt')
    try:
        with open(test_file, 'a') as f:
            f.write("Endpoint called\n")
    except:
        pass
    
    try:
        filter_type = request.args.get('filter', 'today').lower()
        
        # Check for custom date range parameters
        custom_start = request.args.get('start_date')
        custom_end = request.args.get('end_date')
        
        # Calculate date filters for Supabase
        today = datetime.now(timezone.utc).date()
        
        if filter_type == 'custom' and custom_start and custom_end:
            # Use custom date range
            try:
                start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
                end_date = datetime.strptime(custom_end, '%Y-%m-%d').date() + timedelta(days=1)
                print(f"Custom date range: {start_date} to {end_date}")
            except ValueError:
                # Invalid date format, fall back to today
                start_date = today
                end_date = today + timedelta(days=1)
        elif filter_type == 'today':
            start_date = today
            end_date = today + timedelta(days=1)
        elif filter_type == 'yesterday':
            start_date = today - timedelta(days=1)
            end_date = today
        elif filter_type == 'week':
            start_date = today - timedelta(days=7)
            end_date = today + timedelta(days=1)
        elif filter_type == 'month':
            start_date = today - timedelta(days=30)
            end_date = today + timedelta(days=1)
        else:
            start_date = today
            end_date = today + timedelta(days=1)
        
        # Query Supabase
        # Note: To pass multiple conditions on the same field, pass as a list
        # This will create: ?check_in_time=gte.2026-05-04T00:00:00&check_in_time=lt.2026-05-05T00:00:00
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/parking_history",
            headers=SUPABASE_HEADERS,
            params={
                'select': '*',
                'check_in_time': [f'gte.{start_date}T00:00:00', f'lt.{end_date}T00:00:00'],
                'order': 'history_id.desc'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            history = response.json()
            
            # Calculate durations for all records
            total_hours = 0
            total_revenue = 0
            completed_count = 0
            
            for idx, record in enumerate(history):
                if record.get('check_in_time') and record.get('check_out_time'):
                    try:
                        # Parse timestamps - handle both ISO format (T separator) and space format
                        check_in_str = record['check_in_time']
                        check_out_str = record['check_out_time']
                        
                        # Try ISO format first (2026-05-04T18:13:31)
                        try:
                            # Remove timezone info if present, keep naive datetime
                            check_in_clean = check_in_str.replace('Z', '+08:00')
                            check_out_clean = check_out_str.replace('Z', '+08:00')
                            check_in = datetime.fromisoformat(check_in_clean)
                            check_out = datetime.fromisoformat(check_out_clean)
                        except Exception as iso_err:
                            # Fall back to space format (2026-05-04 18:13:31)
                            check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                            check_out = datetime.strptime(check_out_str, '%Y-%m-%d %H:%M:%S')
                        
                        calculated_duration = (check_out - check_in).total_seconds() / 3600
                        record['duration_hours'] = round(calculated_duration, 2)
                        record['parking_fee'] = round(calculated_duration * 5, 2)
                        total_hours += calculated_duration
                        total_revenue += record['parking_fee']
                        completed_count += 1
                    except Exception as e:
                        record['duration_hours'] = 0
                        record['parking_fee'] = 0
                elif record.get('check_in_time') and record.get('status') == 'active':
                    # Currently occupied
                    try:
                        check_in_str = record['check_in_time']
                        # Try ISO format first
                        try:
                            # Remove timezone info if present, keep naive datetime
                            check_in_clean = check_in_str.replace('Z', '+08:00')
                            check_in = datetime.fromisoformat(check_in_clean)
                        except Exception as iso_err:
                            # Fall back to space format
                            check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                        
                        current_duration = (datetime.now(timezone.utc) - check_in).total_seconds() / 3600
                        record['duration_hours'] = round(current_duration, 2)
                        record['parking_fee'] = round(current_duration * 5, 2)
                    except Exception as e:
                        record['duration_hours'] = 0
                        record['parking_fee'] = 0
                else:
                    # No check_out_time and not active
                    record['duration_hours'] = 0
                    record['parking_fee'] = 0
            
            return jsonify({
                'success': True,
                'history': history,
                'filter': filter_type,
                'count': len(history) if history else 0,
                'total_hours': round(total_hours, 2),
                'total_revenue': round(total_revenue, 2),
                'avg_duration': round(total_hours / completed_count, 2) if completed_count > 0 else 0
            })
        else:
            return jsonify({'success': False, 'error': response.text}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get parking rates
@app.route('/api/get_rates', methods=['GET', 'OPTIONS'])
def get_rates():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            cursor.execute("SELECT * FROM parking_rates WHERE status = 'active'")
            rates = cursor.fetchall()
            cursor.close()
            
            return jsonify({'success': True, 'rates': rates})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics - Total Revenue
@app.route('/api/analytics/revenue', methods=['GET', 'OPTIONS'])
@login_required
def analytics_revenue():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Total revenue
            cursor.execute("SELECT COALESCE(SUM(parking_fee), 0) as total_revenue FROM parking_history WHERE status = 'completed'")
            result = cursor.fetchone()
            total_revenue = result['total_revenue'] if result else 0
            
            # Today's revenue
            cursor.execute("""
                SELECT COALESCE(SUM(parking_fee), 0) as today_revenue 
                FROM parking_history 
                WHERE status = 'completed' AND DATE(check_in_time) = CURDATE()
            """)
            today_result = cursor.fetchone()
            today_revenue = today_result['today_revenue'] if today_result else 0
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'total_revenue': float(total_revenue),
                'today_revenue': float(today_revenue)
            })
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics - Parking Sessions
@app.route('/api/analytics/sessions', methods=['GET', 'OPTIONS'])
@login_required
def analytics_sessions():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Get filter parameter (default: today)
            filter_type = request.args.get('filter', 'today').lower()
            
            # Build date filter (PostgreSQL syntax with explicit date range)
            if filter_type == 'today':
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            elif filter_type == 'yesterday':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '1 day' AND check_in_time < CURRENT_DATE"
            elif filter_type == 'week':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '7 days'"
            elif filter_type == 'month':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '30 days'"
            else:
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            
            # Total completed sessions
            cursor.execute(f"SELECT COUNT(*) as total_sessions FROM parking_history WHERE status = 'completed' AND {date_filter}")
            total_result = cursor.fetchone()
            total_sessions = total_result['total_sessions'] if total_result else 0
            
            # Active sessions
            cursor.execute(f"SELECT COUNT(*) as active_sessions FROM parking_history WHERE status = 'active' AND {date_filter}")
            active_result = cursor.fetchone()
            active_sessions = active_result['active_sessions'] if active_result else 0
            
            # Average duration
            cursor.execute(f"""
                SELECT COALESCE(AVG(duration_hours), 0) as avg_duration 
                FROM parking_history 
                WHERE status = 'completed' AND duration_hours IS NOT NULL AND {date_filter}
            """)
            avg_result = cursor.fetchone()
            avg_duration = avg_result['avg_duration'] if avg_result else 0
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'total_sessions': total_sessions,
                'active_sessions': active_sessions,
                'average_duration': float(avg_duration)
            })
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics - Hourly Statistics
@app.route('/api/analytics/hourly', methods=['GET', 'OPTIONS'])
@login_required
def analytics_hourly():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Get filter parameter (default: today)
            filter_type = request.args.get('filter', 'today').lower()
            
            # Build date filter (PostgreSQL syntax with explicit date range)
            if filter_type == 'today':
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            elif filter_type == 'yesterday':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '1 day' AND check_in_time < CURRENT_DATE"
            elif filter_type == 'week':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '7 days'"
            elif filter_type == 'month':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '30 days'"
            else:
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            
            # Get hourly occupancy for selected period
            cursor.execute(f"""
                SELECT EXTRACT(HOUR FROM check_in_time)::int as hour, COUNT(*) as count
                FROM parking_history
                WHERE {date_filter} AND status != 'cancelled'
                GROUP BY EXTRACT(HOUR FROM check_in_time)
                ORDER BY hour
            """)
            hourly_data = cursor.fetchall()
            
            # Format hourly data for chart (0-23 hours, default to 0)
            hourly_stats = [0] * 24
            for row in hourly_data:
                hour = row.get('hour') if isinstance(row, dict) else row[0]
                count = row.get('count') if isinstance(row, dict) else row[1]
                if hour is not None and 0 <= hour < 24:
                    hourly_stats[hour] = int(count) if count else 0
            
            # Get peak hours (top 3 busiest hours)
            peak_hours = []
            if hourly_stats:
                # Create list of (hour, count) tuples
                hour_counts = [(i, hourly_stats[i]) for i in range(24)]
                # Sort by count descending, then by hour
                hour_counts.sort(key=lambda x: (-x[1], x[0]))
                # Get top 3
                peak_hours = hour_counts[:3]
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'hourly_stats': hourly_stats,
                'peak_hours': peak_hours
            })
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics - Occupancy Rate (real-time occupied vs total slots)
@app.route('/api/analytics/occupancy', methods=['GET', 'OPTIONS'])
@login_required
def analytics_occupancy():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Get filter parameter (default: today)
            filter_type = request.args.get('filter', 'today').lower()
            
            # Build date filter (PostgreSQL syntax with explicit date range)
            if filter_type == 'today':
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            elif filter_type == 'yesterday':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '1 day' AND check_in_time < CURRENT_DATE"
            elif filter_type == 'week':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '7 days'"
            elif filter_type == 'month':
                date_filter = "check_in_time >= CURRENT_DATE - INTERVAL '30 days'"
            else:
                date_filter = "check_in_time >= CURRENT_DATE AND check_in_time < CURRENT_DATE + INTERVAL '1 day'"
            
            # Get hourly occupancy rate (occupied vs total slots)
            cursor.execute(f"""
                SELECT 
                  EXTRACT(HOUR FROM check_in_time)::int as hour,
                  COUNT(*) as occupied_count
                FROM parking_history
                WHERE {date_filter} AND status != 'cancelled'
                GROUP BY EXTRACT(HOUR FROM check_in_time)
                ORDER BY hour
            """)
            hourly_data = cursor.fetchall()
            
            # Get total slots
            cursor.execute("SELECT COUNT(*) as total_slots FROM parking_slots")
            total_result = cursor.fetchone()
            total_slots = total_result['total_slots'] if total_result else 1
            
            # Format occupancy rate for chart (0-23 hours, percentage)
            occupancy_rate = [0] * 24
            for row in hourly_data:
                hour = row.get('hour') if isinstance(row, dict) else row[0]
                occupied = row.get('occupied_count') if isinstance(row, dict) else row[1]
                if hour is not None and 0 <= hour < 24:
                    # Calculate percentage: (occupied / total) * 100
                    percentage = (int(occupied) / total_slots * 100) if occupied else 0
                    occupancy_rate[hour] = round(percentage, 2)
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'occupancy_rate': occupancy_rate,
                'total_slots': total_slots
            })
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Change admin password
@app.route('/api/change_password', methods=['POST', 'OPTIONS'])
@login_required
def change_password():
    try:
        if request.method == 'OPTIONS':
            return '', 204
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'success': False, 'error': 'Current and new passwords are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'New password must be at least 6 characters long'}), 400
        
        # Get current user's admin_id from session
        admin_id = session.get('user_id')
        if not admin_id:
            return jsonify({'success': False, 'error': 'User session invalid'}), 401
        
        # Get current admin password using Supabase REST API
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=SUPABASE_HEADERS,
            params={
                'select': 'admin_password',
                'admin_id': f'eq.{admin_id}',
                'limit': 1
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to verify current password'}), 500
        
        admins = response.json()
        if not admins:
            return jsonify({'success': False, 'error': 'Admin not found'}), 404
        
        # Verify current password
        if admins[0]['admin_password'] != current_password:
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 401
        
        # Update password
        update_response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json={
                'admin_password': new_password,
                'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            },
            timeout=10
        )
        
        if update_response.status_code in [200, 204]:
            # Log the action
            try:
                requests.post(
                    f"{SUPABASE_URL}/rest/v1/admin_logs",
                    headers=SUPABASE_HEADERS,
                    json={
                        'admin_id': admin_id,
                        'action': 'change_password',
                        'description': 'Admin changed their password',
                        'created_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    },
                    timeout=10
                )
            except:
                pass  # Log action is optional
            
            return jsonify({'success': True, 'message': 'Password changed successfully'})
        else:
            return jsonify({'success': False, 'error': f'Failed to update password: {update_response.text}'}), 500
            
    except Exception as e:
        print(f"Change password error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Forgot password handler
@app.route('/api/forgot-password', methods=['POST', 'OPTIONS'])
def forgot_password():
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid request data'}), 400
            
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        print(f"🔍 Forgot password request for: {email}")
        
        # Fetch user directly from Supabase using the provided email
        try:
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/admin",
                headers=SUPABASE_HEADERS,
                params={
                    'admin_email': f'eq.{email}',
                    'select': 'admin_id,admin_email,admin_name'
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Database query failed: {response.status_code}")
                return jsonify({'success': False, 'error': 'Database query failed'}), 500
            
            users = response.json()
            
        except requests.exceptions.Timeout:
            print(f"❌ Database query timeout")
            return jsonify({'success': False, 'error': 'Database connection timeout'}), 504
        except requests.exceptions.RequestException as e:
            print(f"❌ Database query error: {e}")
            return jsonify({'success': False, 'error': 'Database connection error'}), 500
        
        if not users or len(users) == 0:
            print(f"ℹ️  Email not found: {email}")
            # For security, don't reveal if email exists or not
            return jsonify({
                'success': True, 
                'message': 'If an account exists with this email, a password reset link will be sent'
            }), 200
        
        # Get the user record - use the SAME user object for everything
        user = users[0]
        admin_id = user['admin_id']
        admin_email = user['admin_email']  # Use email from database, not from input
        admin_name = user['admin_name']    # Use name from database
        
        print(f"✅ User found: {admin_name} ({admin_email})")
        
        # Generate reset token
        reset_token = generate_reset_token()
        
        # Store token in database with expiration (30 minutes)
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        try:
            token_response = requests.post(
                f"{SUPABASE_URL}/rest/v1/password_reset_tokens",
                headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
                json={
                    'admin_id': admin_id,
                    'token': reset_token,
                    'expires_at': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
                },
                timeout=10
            )
            print(f"✅ Reset token stored: {reset_token[:10]}... for admin_id: {admin_id}, name: {admin_name}")
        except Exception as e:
            print(f"⚠️  Error storing reset token: {e}")
            # Continue anyway - we'll still send the email
        
        # Create reset link using request host or BASE_URL
        if request.host:
            protocol = 'https' if request.is_secure else 'http'
            base_url = f"{protocol}://{request.host}"
        else:
            base_url = BASE_URL
        
        reset_link = f"{base_url}/reset-password?token={reset_token}"
        print(f"📧 Preparing reset email for: {admin_email}")
        
        # Send email using the SAME user object
        subject = "Password Reset Request - ParkSlot"
        html_content = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                    <tr>
                        <td align="center">
                            <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                <!-- Header -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #1a4731 0%, #2d6a4f 100%); padding: 30px; text-align: center;">
                                        <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">ParkSlot</h1>
                                        <p style="color: #e8f5e9; margin: 5px 0 0 0; font-size: 14px;">Smart Parking Management System</p>
                                    </td>
                                </tr>
                                
                                <!-- Content -->
                                <tr>
                                    <td style="padding: 40px 30px;">
                                        <h2 style="color: #1a4731; margin: 0 0 20px 0; font-size: 24px;">Password Reset Request</h2>
                                        <p style="color: #333333; line-height: 1.6; margin: 0 0 15px 0;">Hello <strong>{admin_name}</strong>,</p>
                                        <p style="color: #333333; line-height: 1.6; margin: 0 0 25px 0;">We received a request to reset your password. Click the button below to reset it:</p>
                                        
                                        <!-- Button -->
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td align="center" style="padding: 20px 0;">
                                                    <a href="{reset_link}" style="background-color: #1a4731; color: #ffffff; padding: 14px 40px; text-decoration: none; border-radius: 6px; display: inline-block; font-weight: bold; font-size: 16px;">Reset Password</a>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <div style="background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 25px 0; border-radius: 4px;">
                                            <p style="color: #e65100; margin: 0; font-weight: bold; font-size: 14px;">⏰ This link will expire in 30 minutes.</p>
                                        </div>
                                        
                                        <p style="color: #666666; line-height: 1.6; margin: 20px 0 0 0; font-size: 14px;">If you didn't request a password reset, please ignore this email.</p>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: #f9f9f9; padding: 20px 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                        <p style="color: #999999; margin: 0; font-size: 12px;">© 2026 ParkSlot. All rights reserved.</p>
                                        <p style="color: #999999; margin: 5px 0 0 0; font-size: 11px;">This is a system-generated email. Please do not reply.</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        # Return success immediately, send email in background
        # This prevents the request from timing out
        print(f"✅ Returning success response immediately")
        
        # Try to send email but don't wait for it
        import threading
        def send_email_async():
            try:
                print(f"📧 Sending reset email to: {admin_email} (background)")
                email_sent = send_email(admin_email, subject, html_content)
                if email_sent:
                    print(f"✅ Email sent successfully to {admin_email}")
                else:
                    print(f"❌ Email sending failed for {admin_email}")
            except Exception as e:
                print(f"❌ Background email error: {e}")
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_email_async)
        email_thread.daemon = True
        email_thread.start()
        
        # Return success immediately
        return jsonify({
            'success': True, 
            'message': 'Password reset link sent to your email'
        }), 200
            
    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': 'An unexpected error occurred. Please try again later.'}), 500

# Upload admin profile picture
@app.route('/api/upload_profile_picture', methods=['POST', 'OPTIONS'])
@login_required
def upload_profile_picture():
    try:
        if request.method == 'OPTIONS':
            return '', 204
        
        # Check if file exists in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
        
        # Get current user's admin_id from session
        admin_id = session.get('user_id')
        if not admin_id:
            return jsonify({'success': False, 'error': 'User session invalid'}), 401
        
        # Read file content
        file_content = file.read()
        
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': 'File size exceeds 5MB limit'}), 400
        
        # Generate secure filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"admin_{admin_id}_{int(time.time())}.{ext}"
        
        # Save file locally
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Generate public URL
        picture_url = f'/static/images/profiles/{filename}'
        
        # Update database with new picture URL using Supabase REST API
        update_response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json={
                'profile_picture': picture_url,
                'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            },
            timeout=10
        )
        
        if update_response.status_code in [200, 204]:
            # Update session data
            session['profile_picture'] = picture_url
            
            return jsonify({
                'success': True,
                'message': 'Profile picture updated successfully',
                'picture_url': picture_url
            })
        else:
            # Delete the uploaded file if database update fails
            try:
                os.remove(file_path)
            except:
                pass
            return jsonify({'success': False, 'error': f'Database update failed: {update_response.text}'}), 500
            
    except Exception as e:
        print(f"Upload profile picture error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Get admin information
@app.route('/api/get_admin', methods=['GET', 'OPTIONS'])
@login_required
def get_admin():
    try:
        if request.method == 'OPTIONS':
            return '', 204
            
        # Get current user's admin_id from session
        admin_id = session.get('user_id')
        if not admin_id:
            return jsonify({'success': False, 'error': 'User session invalid'}), 401
        
        # Query admin data using Supabase REST API
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=SUPABASE_HEADERS,
            params={
                'select': 'admin_id,admin_name,admin_email,access_level,status,profile_picture',
                'admin_id': f'eq.{admin_id}',
                'limit': 1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            if admins:
                admin = admins[0]
                return jsonify({'success': True, 'admin': admin})
            else:
                return jsonify({'success': False, 'error': 'Admin not found'}), 404
        else:
            return jsonify({'success': False, 'error': f'Database query failed: {response.text}'}), 500
            
    except Exception as e:
        print(f"Get admin error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Logout endpoint
@app.route('/api/logout', methods=['POST', 'OPTIONS'])
def logout():
    """Clear server-side session and log out the user"""
    try:
        if request.method == 'OPTIONS':
            return '', 204
        
        # Get user info before clearing session
        admin_id = session.get('user_id')
        admin_email = session.get('user_email')
        admin_name = session.get('user_name')
        
        # Log the logout action
        logout_timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{'='*60}")
        print(f"🚪 LOGOUT EVENT - {logout_timestamp}")
        print(f"{'='*60}")
        print(f"Admin ID: {admin_id}")
        print(f"Admin Name: {admin_name}")
        print(f"Admin Email: {admin_email}")
        print(f"Session cleared: True")
        print(f"{'='*60}\n")
        
        # Try to log to database
        if admin_id:
            try:
                requests.post(
                    f"{SUPABASE_URL}/rest/v1/admin_logs",
                    headers=SUPABASE_HEADERS,
                    json={
                        'admin_id': admin_id,
                        'action': 'logout',
                        'description': f'User {admin_email} logged out',
                        'created_at': logout_timestamp
                    },
                    timeout=10
                )
            except Exception as log_error:
                print(f"⚠️ Failed to log logout to database: {log_error}")
        
        # Clear all session data
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        print(f"Logout error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Logout redirect route
@app.route('/logout')
def logout_redirect():
    """Clear session and redirect to login page"""
    session.clear()
    return redirect(url_for('index'))

# Session check endpoint
@app.route('/api/check_session', methods=['GET', 'OPTIONS'])
def check_session():
    """Check if user session is valid"""
    try:
        if request.method == 'OPTIONS':
            return '', 204
        
        # Check if user is logged in
        if 'user_id' not in session or 'user_email' not in session:
            return jsonify({
                'success': True,
                'logged_in': False
            })
        
        # Check if account is active
        if session.get('status') != 'active':
            session.clear()
            return jsonify({
                'success': True,
                'logged_in': False
            })
        
        return jsonify({
            'success': True,
            'logged_in': True,
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'user_email': session.get('user_email'),
            'access_level': session.get('access_level'),
            'status': session.get('status', 'active'),
            'profile_picture': session.get('profile_picture', '/static/images/default-profile.png')
        })
    except Exception as e:
        print(f"Session check error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Test Supabase Storage connection
@app.route('/api/test_storage', methods=['GET'])
def test_storage():
    """Test endpoint to verify Supabase Storage bucket exists and is accessible"""
    try:
        # Try to list objects in the avatars bucket
        list_url = f"{SUPABASE_URL}/storage/v1/object/list/avatars"
        
        list_headers = {
            'Authorization': f'Bearer {SUPABASE_API_KEY}',
            'apikey': SUPABASE_API_KEY
        }
        
        response = requests.post(
            list_url,
            headers=list_headers,
            json={'limit': 1, 'offset': 0, 'sortBy': {'column': 'name', 'order': 'asc'}},
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Supabase Storage bucket "avatars" is accessible',
                'bucket_exists': True
            })
        elif response.status_code == 404:
            return jsonify({
                'success': False,
                'message': 'Storage bucket "avatars" not found',
                'bucket_exists': False,
                'instructions': 'Create bucket in Supabase Dashboard: Storage → New bucket → Name: avatars (public)'
            }), 404
        elif response.status_code == 403:
            return jsonify({
                'success': False,
                'message': 'Permission denied - storage policies not set',
                'bucket_exists': True,
                'instructions': 'Set storage policies in Supabase Dashboard: Storage → avatars → Policies'
            }), 403
        else:
            return jsonify({
                'success': False,
                'message': f'Unexpected response: {response.status_code}',
                'details': response.text
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to connect to Supabase Storage'
        }), 500

@app.route('/api/update_admin_info', methods=['POST', 'OPTIONS'])
@login_required
def update_admin_info():
    try:
        if request.method == 'OPTIONS':
            return '', 204
            
        data = request.get_json()
        admin_name = data.get('admin_name', '').strip()
        admin_email = data.get('admin_email', '').strip()
        
        if not admin_name:
            return jsonify({'success': False, 'error': 'Admin name is required'}), 400
        
        if not admin_email or '@' not in admin_email:
            return jsonify({'success': False, 'error': 'Valid email is required'}), 400
        
        # Get current user's admin_id from session
        admin_id = session.get('user_id')
        if not admin_id:
            return jsonify({'success': False, 'error': 'User session invalid'}), 401
        
        # Update admin using Supabase REST API
        update_data = {
            'admin_name': admin_name,
            'admin_email': admin_email,
            'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json=update_data,
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            # Update session data
            session['user_name'] = admin_name
            session['user_email'] = admin_email
            
            return jsonify({'success': True, 'message': 'Admin information updated successfully'})
        else:
            return jsonify({'success': False, 'error': f'Update failed: {response.text}'}), 500
            
    except Exception as e:
        print(f"Update admin info error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Serve HTML pages
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'logo.png',
        mimetype='image/png'
    )

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/parking')
@login_required
def parking():
    return render_template('parking.html')

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Admin Management Page (Super Admin Only)
@app.route('/admin-management')
@super_admin_required
def admin_management():
    return render_template('admin_management.html')

# ============================================
# ADMIN MANAGEMENT API ENDPOINTS
# ============================================

# Get all admins (super_admin only)
@app.route('/api/get_all_admins', methods=['GET'])
@super_admin_required
def get_all_admins():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=SUPABASE_HEADERS,
            params={'select': 'admin_id,admin_name,admin_email,access_level,status,profile_picture,last_login,created_at,created_by'},
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            return jsonify({'success': True, 'admins': admins})
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch admins'}), 500
            
    except Exception as e:
        print(f"Get all admins error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Create new admin (super_admin only)
@app.route('/api/create_admin', methods=['POST'])
@super_admin_required
def create_admin():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['admin_name', 'admin_email', 'admin_password', 'access_level']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # Validate email format
        if '@' not in data['admin_email']:
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Validate access level
        valid_levels = ['super_admin', 'admin', 'manager']
        if data['access_level'] not in valid_levels:
            return jsonify({'success': False, 'error': 'Invalid access level'}), 400
        
        # Check if email already exists
        check_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=SUPABASE_HEADERS,
            params={'admin_email': f"eq.{data['admin_email']}", 'select': 'admin_id'},
            timeout=10
        )
        
        if check_response.status_code == 200 and len(check_response.json()) > 0:
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        # Create new admin
        new_admin = {
            'admin_name': data['admin_name'],
            'admin_email': data['admin_email'],
            'admin_password': data['admin_password'],  # In production, hash this!
            'access_level': data['access_level'],
            'status': 'active',
            'created_by': data.get('created_by', 1),  # Current admin ID
            'profile_picture': '/static/images/default-profile.png'
        }
        
        create_response = requests.post(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            json=new_admin,
            timeout=10
        )
        
        if create_response.status_code in [200, 201]:
            created_admin = create_response.json()[0] if isinstance(create_response.json(), list) else create_response.json()
            return jsonify({
                'success': True,
                'message': 'Admin created successfully',
                'admin': created_admin
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to create admin'}), 500
            
    except Exception as e:
        print(f"Create admin error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Update admin details (super_admin only)
@app.route('/api/update_admin', methods=['POST'])
@super_admin_required
def update_admin():
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        if not admin_id:
            return jsonify({'success': False, 'error': 'admin_id is required'}), 400
        
        # Build update object (only include provided fields)
        update_data = {}
        if 'admin_name' in data:
            update_data['admin_name'] = data['admin_name']
        if 'admin_email' in data:
            update_data['admin_email'] = data['admin_email']
        if 'access_level' in data:
            update_data['access_level'] = data['access_level']
        if 'status' in data:
            update_data['status'] = data['status']
        
        if not update_data:
            return jsonify({'success': False, 'error': 'No fields to update'}), 400
        
        # Update admin
        update_response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json=update_data,
            timeout=10
        )
        
        if update_response.status_code in [200, 204]:
            # Fetch the updated admin record
            get_response = requests.get(
                f"{SUPABASE_URL}/rest/v1/admin",
                headers=SUPABASE_HEADERS,
                params={'admin_id': f'eq.{admin_id}', 'select': '*'},
                timeout=10
            )
            
            updated_admin = None
            if get_response.status_code == 200 and len(get_response.json()) > 0:
                updated_admin = get_response.json()[0]
            
            return jsonify({
                'success': True,
                'message': 'Admin updated successfully',
                'admin': updated_admin
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update admin'}), 500
            
    except Exception as e:
        print(f"Update admin error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Delete admin (super_admin only)
@app.route('/api/delete_admin', methods=['POST'])
@super_admin_required
def delete_admin():
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        if not admin_id:
            return jsonify({'success': False, 'error': 'admin_id is required'}), 400
        
        # Prevent deleting admin_id = 1 (super admin)
        if admin_id == 1:
            return jsonify({'success': False, 'error': 'Cannot delete super admin'}), 400
        
        # Delete admin
        delete_response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers=SUPABASE_HEADERS,
            params={'admin_id': f'eq.{admin_id}'},
            timeout=10
        )
        
        if delete_response.status_code in [200, 204]:
            return jsonify({
                'success': True,
                'message': 'Admin deleted successfully',
                'admin_id': admin_id
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete admin'}), 500
            
    except Exception as e:
        print(f"Delete admin error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Reset admin password (super_admin only)
@app.route('/api/reset_admin_password', methods=['POST'])
@super_admin_required
def reset_admin_password():
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        new_password = data.get('new_password')
        
        if not admin_id or not new_password:
            return jsonify({'success': False, 'error': 'admin_id and new_password are required'}), 400
        
        # Update password (in production, hash this!)
        update_response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json={'admin_password': new_password},
            timeout=10
        )
        
        if update_response.status_code in [200, 204]:
            return jsonify({
                'success': True,
                'message': 'Password reset successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to reset password'}), 500
            
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Update admin profile with picture upload (super_admin only)
@app.route('/api/update_admin_profile', methods=['POST', 'OPTIONS'])
@super_admin_required
def update_admin_profile():
    try:
        if request.method == 'OPTIONS':
            return '', 204
            
        admin_id = request.form.get('admin_id')
        admin_name = request.form.get('admin_name')
        admin_email = request.form.get('admin_email')
        access_level = request.form.get('access_level')
        status = request.form.get('status')
        
        if not admin_id or not admin_name or not admin_email:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Validate email format
        if '@' not in admin_email:
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400
        
        # Validate access level
        valid_access_levels = ['super_admin', 'admin', 'manager']
        if access_level and access_level not in valid_access_levels:
            return jsonify({'success': False, 'error': 'Invalid access level'}), 400
        
        # Validate status
        valid_statuses = ['active', 'inactive', 'suspended']
        if status and status not in valid_statuses:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        # Handle profile picture upload
        profile_picture_url = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename and allowed_file(file.filename):
                # Check file size
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                if file_size > MAX_FILE_SIZE:
                    return jsonify({'success': False, 'error': 'File too large. Maximum size is 5MB'}), 400
                
                # Generate secure filename
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                filename = f"{admin_id}_{timestamp}_{filename}"
                
                # Save file locally
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Set profile picture URL
                profile_picture_url = f'/static/images/profiles/{filename}'
        
        # Prepare update data
        update_data = {
            'admin_name': admin_name,
            'admin_email': admin_email,
            'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add password if provided
        admin_password = request.form.get('admin_password')
        if admin_password:
            update_data['admin_password'] = admin_password
        
        # Add access level if provided
        if access_level:
            update_data['access_level'] = access_level
        
        # Add status if provided
        if status:
            update_data['status'] = status
        
        # Add profile picture if uploaded
        if profile_picture_url:
            update_data['profile_picture'] = profile_picture_url
        
        # Update admin profile using Supabase REST API
        update_response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/admin",
            headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
            params={'admin_id': f'eq.{admin_id}'},
            json=update_data,
            timeout=10
        )
        
        if update_response.status_code in [200, 204]:
            # Fetch the updated admin record
            get_response = requests.get(
                f"{SUPABASE_URL}/rest/v1/admin",
                headers=SUPABASE_HEADERS,
                params={'admin_id': f'eq.{admin_id}', 'select': '*'},
                timeout=10
            )
            
            updated_admin = None
            if get_response.status_code == 200 and len(get_response.json()) > 0:
                updated_admin = get_response.json()[0]
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'picture_url': profile_picture_url,
                'admin': updated_admin
            })
        else:
            # Delete uploaded file if database update fails
            if profile_picture_url:
                try:
                    os.remove(file_path)
                except:
                    pass
            return jsonify({'success': False, 'error': f'Failed to update profile: {update_response.text}'}), 500
        
    except Exception as e:
        print(f"Update admin profile error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Handle preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

# Reset password page (GET)
# Reset password page (GET)
@app.route('/reset-password', methods=['GET'])
def reset_password_page():
    token = request.args.get('token')
    if not token:
        return render_template('error.html', message='Invalid or missing reset token'), 400
    
    # For now, accept any token format (simplified for testing)
    # In production, validate against database
    
    try:
        connection = get_db_connection()
        if connection is None:
            # Still show form even if DB is down
            return render_template('reset_password.html', token=token)
        
        cursor = get_db_cursor(connection)
        
        # Try to validate token from database
        try:
            cursor.execute(
                "SELECT admin_id FROM password_reset_tokens WHERE token = %s AND expires_at > NOW()",
                (token,)
            )
            result = cursor.fetchone()
            
            if result:
                # Token is valid
                cursor.close()
                connection.close()
                return render_template('reset_password.html', token=token)
        except Exception as e:
            print(f"Token validation error: {e}")
        
        cursor.close()
        connection.close()
        
        # If token not found in DB, still allow reset with token
        # (simplified for testing - in production, reject invalid tokens)
        return render_template('reset_password.html', token=token)
        
    except Exception as e:
        print(f"Reset password page error: {e}")
        # Still show form even on error
        return render_template('reset_password.html', token=token)

# Reset password API (POST)
@app.route('/api/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not all([token, new_password, confirm_password]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        if new_password != confirm_password:
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400
        
        if not any(c.isupper() for c in new_password):
            return jsonify({'success': False, 'error': 'Password must contain at least 1 uppercase letter'}), 400
        
        if not any(c.islower() for c in new_password):
            return jsonify({'success': False, 'error': 'Password must contain at least 1 lowercase letter'}), 400
        
        if not any(c.isdigit() for c in new_password):
            return jsonify({'success': False, 'error': 'Password must contain at least 1 number'}), 400
        
        if not any(c in '!@#$%^&*(),.?":{}|<>' for c in new_password):
            return jsonify({'success': False, 'error': 'Password must contain at least 1 special character'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Verify token exists and is not expired
            cursor.execute(
                "SELECT admin_id FROM password_reset_tokens WHERE token = %s AND expires_at > NOW()",
                (token,)
            )
            result = cursor.fetchone()
            
            if not result:
                return jsonify({'success': False, 'error': 'Token is invalid or has expired'}), 400
            
            admin_id = result['admin_id']
            
            # Get admin email and name
            cursor.execute(
                "SELECT admin_email, admin_name FROM admin WHERE admin_id = %s",
                (admin_id,)
            )
            admin_info = cursor.fetchone()
            
            if not admin_info:
                return jsonify({'success': False, 'error': 'Admin account not found'}), 400
            
            admin_email = admin_info['admin_email']
            admin_name = admin_info['admin_name']
            
            # Update password
            cursor.execute(
                "UPDATE admin SET admin_password = %s WHERE admin_id = %s",
                (new_password, admin_id)
            )
            
            # Delete used token
            cursor.execute("DELETE FROM password_reset_tokens WHERE token = %s", (token,))
            
            # Log the action
            cursor.execute(
                "INSERT INTO admin_logs (admin_id, action, description) VALUES (%s, %s, %s)",
                (admin_id, 'password_reset', 'Password was reset via email link')
            )
            
            connection.commit()
            cursor.close()
            
            # Send confirmation email
            subject = "Password Reset Confirmation - ParkSlot"
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #1B4D3E;">Password Reset Successful</h2>
                        <p>Hello {admin_name},</p>
                        <p>Your password has been successfully reset. You can now login to your ParkSlot account with your new password.</p>
                        <div style="background-color: #ECFDF5; border-left: 4px solid #065F46; padding: 15px; margin: 20px 0; border-radius: 5px;">
                            <p style="color: #065F46; margin: 0;">
                                <strong>✓ Password Reset Complete</strong><br>
                                If you did not request this password reset, please contact support immediately.
                            </p>
                        </div>
                        <h3 style="color: #1B4D3E; font-size: 1rem; margin-top: 25px;">Next Steps:</h3>
                        <ol style="color: #4B5563;">
                            <li>Close this window and return to the login page</li>
                            <li>Sign in with your email: <strong>{admin_email}</strong></li>
                            <li>Use your new password to access your account</li>
                        </ol>
                        <div style="background-color: #FEF2F2; border-left: 4px solid #B91C1C; padding: 15px; margin: 20px 0; border-radius: 5px;">
                            <p style="color: #B91C1C; margin: 0;">
                                <strong>⚠ Security Note:</strong><br>
                                Never share your password with anyone. ParkSlot staff will never ask for your password.
                            </p>
                        </div>
                        <p style="font-size: 0.9rem; color: #666; margin-top: 25px;">
                            If you have any questions or concerns about your account security, please contact our support team.
                        </p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 0.8rem; color: #999; margin: 0;">
                            © 2026 ParkSlot. All rights reserved.<br>
                            Smart Parking Slot Management System
                        </p>
                    </div>
                </body>
            </html>
            """
            
            send_email(admin_email, subject, html_content)
            
            return jsonify({
                'success': True, 
                'message': 'Password reset successfully. A confirmation email has been sent.'
            }), 200
            
        finally:
            connection.close()
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Create password reset tokens table on startup
def create_password_reset_table():
    """Skip startup verification to avoid blocking app launch on network issues."""
    print("Password reset table check skipped at startup")

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
    
    print(f"\n{'='*70}")
    print(f"🚀 Starting ParkSlot Application")
    print(f"{'='*70}")
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: Supabase REST API")
    print(f"{'='*70}")
    print(f"\n✅ Access your app at:")
    print(f"   Local:        http://localhost:{port}")
    print(f"   Local Network: http://YOUR_LOCAL_IP:{port}")
    print(f"   Health Check: http://localhost:{port}/api/health")
    print(f"{'='*70}\n")
    
    # Run Flask app
    app.run(
        debug=debug,
        host=host,
        port=port,
        threaded=True,
        use_reloader=debug
    )