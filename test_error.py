#!/usr/bin/env python3
import requests
import json

r = requests.get("http://localhost:5000/api/get_history_filtered?filter=today")
print(f"Status: {r.status_code}")
d = r.json()
print(f"Error: {d.get('error')}")
