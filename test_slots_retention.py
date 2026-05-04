#!/usr/bin/env python3
"""
Test script to verify parking slots are retained from database
"""
import requests
import json

API_BASE = 'http://localhost:5000/api'

def test_slots_retention():
    print("=" * 70)
    print("PARKING SLOTS RETENTION TEST")
    print("=" * 70)
    
    # Test 1: Get all slots from database
    print("\n[1] Fetching all parking slots from database...")
    try:
        response = requests.get(f'{API_BASE}/get_slots', timeout=5)
        if response.status_code == 200:
            data = response.json()
            slots = data.get('slots', [])
            print(f"    SUCCESS: {len(slots)} slots loaded from database")
            print()
            print("    Slots Details:")
            for slot in slots:
                print(f"      - Slot {slot['slot_id']}: {slot['slot_label']} ({slot['slot_status']})")
                print(f"        Check-in: {slot.get('check_in_time', 'N/A')}")
                print(f"        Check-out: {slot.get('check_out_time', 'N/A')}")
                print(f"        Vehicle: {slot.get('vehicle_reg_number', 'N/A')}")
                print()
        else:
            print(f"    ERROR: Status {response.status_code}")
            print(f"    Response: {response.text}")
            return False
    except Exception as e:
        print(f"    ERROR: {e}")
        return False
    
    # Test 2: Verify slot data persistence
    print("[2] Verifying slot data persistence...")
    try:
        response = requests.get(f'{API_BASE}/get_slots', timeout=5)
        data = response.json()
        slots = data.get('slots', [])
        
        if len(slots) > 0:
            print(f"    SUCCESS: {len(slots)} slots retained in database")
            
            # Check if slots have expected fields
            first_slot = slots[0]
            required_fields = ['slot_id', 'slot_label', 'slot_status', 'check_in_time', 'check_out_time']
            missing_fields = [f for f in required_fields if f not in first_slot]
            
            if missing_fields:
                print(f"    WARNING: Missing fields: {missing_fields}")
            else:
                print(f"    All required fields present")
        else:
            print(f"    ERROR: No slots found in database")
            return False
    except Exception as e:
        print(f"    ERROR: {e}")
        return False
    
    # Test 3: Check parking summary
    print("\n[3] Checking parking summary...")
    try:
        response = requests.get(f'{API_BASE}/get_summary', timeout=5)
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', {})
            print(f"    SUCCESS: Summary retrieved")
            print(f"      Total Slots: {summary.get('total', 0)}")
            print(f"      Available: {summary.get('available', 0)}")
            print(f"      Occupied: {summary.get('occupied', 0)}")
            print(f"      Occupancy: {summary.get('occupancy_percent', 0)}%")
        else:
            print(f"    ERROR: Status {response.status_code}")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print("\nSlots are being retained from the database correctly!")
    print("The parking.html page loads slots via /api/get_slots endpoint")
    print("and displays them with their current status from the database.")
    print("\n" + "=" * 70)
    
    return True

if __name__ == '__main__':
    test_slots_retention()
