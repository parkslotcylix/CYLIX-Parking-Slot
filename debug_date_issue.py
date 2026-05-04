#!/usr/bin/env python3
import requests
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

# Get history
response = requests.get(f'{API_BASE}/get_history', timeout=5)
if response.status_code == 200:
    data = response.json()
    history = data.get('history', [])
    
    if history:
        # Check first record
        first = history[0]
        print(f"First record:")
        print(f"  history_id: {first.get('history_id')}")
        print(f"  check_in_time: {first.get('check_in_time')}")
        print(f"  check_in_time type: {type(first.get('check_in_time'))}")
        print(f"  status: {first.get('status')}")
        
        # Try to parse the date
        check_in = first.get('check_in_time')
        if check_in:
            try:
                # Try different formats
                formats = [
                    '%a, %d %b %Y %H:%M:%S %Z',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%dT%H:%M:%S',
                ]
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(check_in, fmt)
                        print(f"\nParsed with format: {fmt}")
                        print(f"  Date: {dt.date()}")
                        print(f"  Time: {dt.time()}")
                        break
                    except:
                        continue
            except Exception as e:
                print(f"Error parsing: {e}")
        
        # Check today's date
        today = datetime.now().date()
        print(f"\nToday's date: {today}")
        print(f"Today's date (ISO): {today.isoformat()}")
