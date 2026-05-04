#!/usr/bin/env python3
"""
Simple verification script to check if parking history system is working
"""
import requests
import json
import time
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

def verify_system():
    """Verify the parking history system is working"""
    
    print("=" * 60)
    print("PARKING HISTORY SYSTEM VERIFICATION")
    print("=" * 60)
    
    # Test 1: Check if API is responding
    print("\n[1] Checking API connectivity...")
    try:
        response = requests.get(f'{API_BASE}/get_summary', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("    SUCCESS: API is responding")
            print(f"    Summary: {data}")
        else:
            print(f"    ERROR: API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"    ERROR: Cannot connect to API - {e}")
        print("    Make sure Flask app is running on http://localhost:5000")
        return False
    
    # Test 2: Check analytics endpoints
    print("\n[2] Checking analytics endpoints...")
    try:
        response = requests.get(f'{API_BASE}/analytics/sessions', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("    SUCCESS: Analytics sessions endpoint working")
            print(f"    Total Sessions: {data.get('total_sessions')}")
            print(f"    Active Sessions: {data.get('active_sessions')}")
            print(f"    Average Duration: {data.get('average_duration')} hours")
        else:
            print(f"    ERROR: Endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Test 3: Check parking history
    print("\n[3] Checking parking history...")
    try:
        response = requests.get(f'{API_BASE}/get_history', timeout=5)
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            print(f"    SUCCESS: Found {len(history)} parking history records")
            if history:
                print(f"    Latest record: {history[0]}")
        else:
            print(f"    ERROR: Endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Test 4: Test toggle functionality
    print("\n[4] Testing slot toggle functionality...")
    try:
        slot_id = 1
        
        # Toggle to occupied
        print(f"    Toggling slot {slot_id} to OCCUPIED...")
        response = requests.post(
            f'{API_BASE}/toggle_slot',
            json={'slot_id': slot_id},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"    SUCCESS: {data}")
            
            # Wait
            time.sleep(1)
            
            # Toggle back to available
            print(f"    Toggling slot {slot_id} back to AVAILABLE...")
            response = requests.post(
                f'{API_BASE}/toggle_slot',
                json={'slot_id': slot_id},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"    SUCCESS: {data}")
                print("\n    PARKING HISTORY RECORD SHOULD NOW BE CREATED!")
            else:
                print(f"    ERROR: Toggle back failed - {response.status_code}")
        else:
            print(f"    ERROR: Toggle failed - {response.status_code}")
            print(f"    Response: {response.text}")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check Supabase Dashboard for parking_history records")
    print("2. Visit http://localhost:5000/analytics to view the report")
    print("3. Click 'Print Analytics Report' to generate PDF")
    print("=" * 60)

if __name__ == '__main__':
    verify_system()
