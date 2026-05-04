#!/usr/bin/env python3
import requests

r = requests.get("http://localhost:5000/api/get_history_filtered?filter=today")
d = r.json()
history = d.get('history', [])

print(f"Total records: {len(history)}")
print(f"\nFirst 5 records:")
for i, record in enumerate(history[:5]):
    check_in = record.get('check_in_time')
    check_out = record.get('check_out_time')
    status = record.get('status')
    duration = record.get('duration_hours')
    print(f"{i}: check_in={check_in}, check_out={check_out}, status={status}, duration={duration}")

# Check what records don't have check_out_time
no_checkout = [r for r in history if not r.get('check_out_time')]
print(f"\n\nRecords without check_out_time: {len(no_checkout)}")
for r in no_checkout[:3]:
    print(f"  - ID {r['history_id']}: status={r.get('status')}, check_in={r.get('check_in_time')}")

# Check what records don't have check_in_time
no_checkin = [r for r in history if not r.get('check_in_time')]
print(f"Records without check_in_time: {len(no_checkin)}")
