#!/usr/bin/env python3
"""
Create test parking history data for today to test filters
"""
import requests
import time
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

def create_test_data():
    print("=" * 70)
    print("CREATING TEST DATA FOR TODAY")
    print("=" * 70)
    
    # Toggle slots to create parking history for today
    print("\nCreating parking sessions for today...")
    
    for slot_id in [1, 2, 3]:
        print(f"\n[Slot {slot_id}]")
        
        # Toggle to Occupied
        print(f"  1. Setting slot {slot_id} to OCCUPIED...")
        try:
            response = requests.post(
                f'{API_BASE}/toggle_slot',
                json={'slot_id': slot_id},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"     SUCCESS: {data.get('new_status')}")
            else:
                print(f"     ERROR: {response.status_code}")
        except Exception as e:
            print(f"     ERROR: {e}")
        
        # Wait a moment
        time.sleep(1)
        
        # Toggle back to Available
        print(f"  2. Setting slot {slot_id} to AVAILABLE...")
        try:
            response = requests.post(
                f'{API_BASE}/toggle_slot',
                json={'slot_id': slot_id},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"     SUCCESS: {data.get('new_status')}")
            else:
                print(f"     ERROR: {response.status_code}")
        except Exception as e:
            print(f"     ERROR: {e}")
        
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("TEST DATA CREATED")
    print("=" * 70)
    
    # Verify data was created
    print("\nVerifying data for TODAY filter...")
    try:
        response = requests.get(f'{API_BASE}/analytics/sessions?filter=today', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Sessions: {data.get('total_sessions')}")
            print(f"  Active Sessions: {data.get('active_sessions')}")
            print(f"  Avg Duration: {data.get('average_duration')} hours")
            
            if data.get('total_sessions') > 0:
                print("\n✅ SUCCESS: Today filter now has data!")
            else:
                print("\n⚠ WARNING: No data for today yet")
        else:
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == '__main__':
    create_test_data()
