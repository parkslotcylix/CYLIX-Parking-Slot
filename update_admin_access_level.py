#!/usr/bin/env python3
"""Quick script to update admin account access level for 2FA testing"""

import requests
import os
from dotenv import load_dotenv

load_dotenv(override=False)

# Supabase config
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://bhsofudngyukxkkialwi.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJoc29mdWRuZ3l1a3hra2lhbHdpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzYxNDg4MywiZXhwIjoyMDkzMTkwODgzfQ.BcwHm7lt6fj0FD6Zd2LAzA9aGd3KLxW7mPfhhw94OGk')

HEADERS = {
    'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
    'Content-Type': 'application/json',
    'apikey': SUPABASE_SERVICE_ROLE_KEY
}

# Update this email to the account you want to enable 2FA for
EMAIL = 'jbillones.k12149156@umak.edu.ph'

def get_admin_by_email(email):
    """Get admin by email"""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/admin",
        headers=HEADERS,
        params={
            'select': 'admin_id,admin_email,access_level',
            'admin_email': f'eq.{email}',
            'limit': 1
        },
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        return results[0] if results else None
    else:
        print(f"❌ Error fetching admin: {response.status_code}")
        print(response.text)
        return None

def update_admin_access_level(admin_id, new_access_level):
    """Update admin access level"""
    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/admin?admin_id=eq.{admin_id}",
        headers=HEADERS,
        json={'access_level': new_access_level},
        timeout=10
    )
    
    if response.status_code in [200, 204]:
        print(f"✅ Admin access level updated successfully!")
        return True
    else:
        print(f"❌ Error updating admin: {response.status_code}")
        print(response.text)
        return False

def main():
    print(f"🔍 Looking for admin: {EMAIL}")
    
    admin = get_admin_by_email(EMAIL)
    
    if not admin:
        print(f"❌ Admin not found with email: {EMAIL}")
        return
    
    print(f"✅ Found admin:")
    print(f"   ID: {admin['admin_id']}")
    print(f"   Email: {admin['admin_email']}")
    print(f"   Current Access Level: {admin['access_level']}")
    
    if admin['access_level'].lower() == 'admin':
        print(f"✅ Access level is already 'admin' - 2FA should be enabled!")
        return
    
    print(f"\n🔄 Updating access level to 'admin'...")
    
    if update_admin_access_level(admin['admin_id'], 'admin'):
        print(f"✅ Done! Now login with {EMAIL} - you should see the 2FA verification form!")
    else:
        print(f"❌ Failed to update access level")

if __name__ == '__main__':
    main()
