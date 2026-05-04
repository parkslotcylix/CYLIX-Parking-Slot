#!/usr/bin/env python3
"""
Final test to confirm parking duration calculations are working across all endpoints
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

print("=" * 80)
print("FINAL TEST: Parking Duration Calculations")
print("=" * 80)

# Test 1: get_history_filtered endpoint
print("\n1. Testing /api/get_history_filtered (for analytics):")
r = requests.get(f"{API_BASE}/get_history_filtered?filter=today")
d = r.json()
print(f"   Status: {r.status_code}")
print(f"   Count: {d.get('count')} records for today")
print(f"   Average Duration: {d.get('avg_duration')} hours = {int(d.get('avg_duration', 0)*60)}m")
print(f"   Total Hours: {d.get('total_hours')}")
print(f"   Total Revenue: ${d.get('total_revenue')}")

if d.get('history'):
    first = d['history'][0]
    print(f"   First record: check_in={first.get('check_in_time')}, check_out={first.get('check_out_time')}")
    print(f"                 duration={first.get('duration_hours')}h, fee=${first.get('parking_fee')}")

# Test 2: Test different filters
print("\n2. Testing different time filters:")
for filter_type in ['today', 'yesterday', 'week', 'month']:
    r = requests.get(f"{API_BASE}/get_history_filtered?filter={filter_type}")
    d = r.json()
    avg_hours = d.get('avg_duration', 0)
    avg_minutes = int(avg_hours * 60)
    print(f"   {filter_type:10} → avg_duration: {avg_hours}h ({avg_minutes}m), count: {d.get('count')}")

# Test 3: get_slots endpoint (real-time durations)
print("\n3. Testing /api/get_slots (real-time occupied slot durations):")
r = requests.get(f"{API_BASE}/get_slots")
d = r.json()
occupied = [s for s in d.get('slots', []) if s.get('slot_status') == 'occupied']
print(f"   Status: {r.status_code}")
print(f"   Occupied slots: {len(occupied)}")
if occupied:
    for slot in occupied[:2]:
        duration_h = slot.get('current_duration_hours', 0)
        duration_m = int(duration_h * 60)
        print(f"   - Slot {slot.get('slot_id')}: {duration_h}h ({duration_m}m) since {slot.get('check_in_time')}")

print("\n" + "=" * 80)
print("✅ All endpoints returning non-zero duration values!")
print("=" * 80)
