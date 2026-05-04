#!/usr/bin/env python3
import requests
import json
import os

r = requests.get("http://localhost:5000/api/get_history_filtered?filter=today")
print(f"Status: {r.status_code}")
d = r.json()
print(f"avg_duration: {d.get('avg_duration')}")
print(f"count: {d.get('count')}")
print(f"First record duration: {d['history'][0]['duration_hours'] if d.get('history') else 'N/A'}")
print(f"Has error key: {'error' in d}")

# Check if debug log exists
debug_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'debug_filtered.log'))
print(f"\nLooking for debug log at: {debug_path}")
if os.path.exists(debug_path):
    with open(debug_path, 'r') as f:
        content = f.read()
        print(f"Debug log contents ({len(content)} bytes):\n{content}")
else:
    print(f"Debug log NOT FOUND")
    print(f"Files in current dir: {os.listdir('.')}")

