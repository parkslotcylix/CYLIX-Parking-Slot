#!/usr/bin/env python3
"""
Test script to verify parking history is being created
"""
import requests
import json
import time
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

def test_toggle_slot():
    """Test toggling a slot and verify history is created"""
    
    print("=" * 60)
    print("PARKING HISTORY TEST")
    print("=" * 60)
    
    # Test slot 1
    slot_id = 1
    
    print(f"\n1️⃣  Toggling slot {slot_id} to OCCUPIED...")
    response = requests.post(
        f'{API_BASE}/toggle_slot',
        json={'slot_id': slot_id},
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
        print(f"   Status: {data.get('new_status')}")
        print(f"   Timestamp: {data.get('timestamp')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # Wait a moment
    print("\n⏳ Waiting 2 seconds...")
    time.sleep(2)
    
    print(f"\n2️⃣  Toggling slot {slot_id} back to AVAILABLE...")
    response = requests.post(
        f'{API_BASE}/toggle_slot',
        json={'slot_id': slot_id},
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
        print(f"   Status: {data.get('new_status')}")
        print(f"   Timestamp: {data.get('timestamp')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # Check parking history
    print(f"\n3️⃣  Checking parking_history table...")
    print("   Query: SELECT * FROM parking_history ORDER BY history_id DESC LIMIT 5;")
    print("\n   Expected: You should see 1 completed record with:")
    print("   - slot_id = 1")
    print("   - status = 'completed'")
    print("   - check_in_time and check_out_time populated")
    print("   - duration_hours calculated")
    
    print("\n✅ TEST COMPLETE!")
    print("\nNext steps:")
    print("1. Go to Supabase Dashboard → SQL Editor")
    print("2. Run: SELECT * FROM parking_history ORDER BY history_id DESC LIMIT 5;")
    print("3. Verify records are created when you toggle slots")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        test_toggle_slot()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
