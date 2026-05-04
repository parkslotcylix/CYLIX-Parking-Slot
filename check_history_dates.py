#!/usr/bin/env python3
import requests
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

# Get all history
response = requests.get(f'{API_BASE}/get_history', timeout=5)
if response.status_code == 200:
    data = response.json()
    history = data.get('history', [])
    print(f'Total records: {len(history)}')
    print('\nLast 10 records:')
    for record in history[:10]:
        check_in = record.get('check_in_time')
        status = record.get('status')
        slot_id = record.get('slot_id')
        history_id = record.get('history_id')
        
        # Parse date
        if check_in:
            try:
                dt = datetime.strptime(check_in, '%a, %d %b %Y %H:%M:%S %Z')
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = check_in
        else:
            date_str = 'N/A'
        
        print(f'  ID: {history_id}, Slot: {slot_id}, Date: {date_str}, Status: {status}')
    
    # Check today's date
    today = datetime.now().strftime('%Y-%m-%d')
    print(f'\nToday is: {today}')
    
    # Count records for today
    today_count = 0
    for record in history:
        check_in = record.get('check_in_time')
        if check_in:
            try:
                dt = datetime.strptime(check_in, '%a, %d %b %Y %H:%M:%S %Z')
                if dt.strftime('%Y-%m-%d') == today:
                    today_count += 1
            except:
                pass
    
    print(f'Records for today: {today_count}')
