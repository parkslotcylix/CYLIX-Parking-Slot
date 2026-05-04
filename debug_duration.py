#!/usr/bin/env python3
import requests
from datetime import datetime

# Simulate what the API endpoint does
SUPABASE_URL = "https://nohawgvnvkvxuuqvwixd.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5vaGF3Z3Zudmtmedh1dXF2d2l4ZCIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzE1MTI0Nzc2LCJleHAiOjE4NzI5MDI3NzZ9.5f7A4H9X2u-RTGHJhXX8M1QVzRBDtEZDMxE6X5Y8KYI"

SUPABASE_HEADERS = {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_API_KEY,
    'Authorization': f'Bearer {SUPABASE_API_KEY}',
}

today = datetime.now().date()
start_date = today
end_date = today

print(f"Querying for filter: today")
print(f"Date range: {start_date} to {end_date}")

# Query Supabase
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/parking_history",
    headers=SUPABASE_HEADERS,
    params={
        'select': '*',
        'check_in_time': f'gte.{start_date}T00:00:00',
        'check_in_time': f'lt.{end_date}T00:00:00',
        'order': 'history_id.desc'
    },
    timeout=10
)

print(f"\nResponse status: {response.status_code}")

if response.status_code == 200:
    history = response.json()
    print(f"Records retrieved: {len(history)}")
    
    # Calculate durations for all records
    total_hours = 0
    total_revenue = 0
    completed_count = 0
    
    for i, record in enumerate(history[:3]):  # Just test first 3
        print(f"\n--- Record {i+1} (ID: {record.get('history_id')}) ---")
        print(f"check_in_time: {record.get('check_in_time')}")
        print(f"check_out_time: {record.get('check_out_time')}")
        print(f"status: {record.get('status')}")
        
        if record.get('check_in_time') and record.get('check_out_time'):
            try:
                # Parse timestamps - handle both ISO format (T separator) and space format
                check_in_str = record['check_in_time']
                check_out_str = record['check_out_time']
                
                print(f"  Parsing check_in: '{check_in_str}'")
                print(f"  Parsing check_out: '{check_out_str}'")
                
                # Try ISO format first (2026-05-04T18:13:31)
                try:
                    # Remove timezone info if present, keep naive datetime
                    check_in_clean = check_in_str.replace('Z', '').replace('+00:00', '')
                    check_out_clean = check_out_str.replace('Z', '').replace('+00:00', '')
                    print(f"  Cleaned check_in: '{check_in_clean}'")
                    print(f"  Cleaned check_out: '{check_out_clean}'")
                    check_in = datetime.fromisoformat(check_in_clean)
                    check_out = datetime.fromisoformat(check_out_clean)
                    print(f"  Parsed as ISO format")
                except Exception as iso_err:
                    # Fall back to space format (2026-05-04 18:13:31)
                    print(f"  ISO parse failed ({iso_err}), trying space format")
                    check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                    check_out = datetime.strptime(check_out_str, '%Y-%m-%d %H:%M:%S')
                
                calculated_duration = (check_out - check_in).total_seconds() / 3600
                print(f"  Duration hours: {calculated_duration}")
                record['duration_hours'] = round(calculated_duration, 2)
                record['parking_fee'] = round(calculated_duration * 5, 2)
                total_hours += calculated_duration
                total_revenue += record['parking_fee']
                completed_count += 1
                print(f"  Stored duration_hours: {record['duration_hours']}")
            except Exception as e:
                print(f"  Error parsing duration: {e}")
                record['duration_hours'] = 0
                record['parking_fee'] = 0
        elif record.get('check_in_time') and record.get('status') == 'active':
            print(f"  Active session (no check_out)")
        else:
            print(f"  No check_in or incomplete record")
    
    print(f"\n\nFinal Summary:")
    print(f"Total hours: {total_hours}")
    print(f"Completed count: {completed_count}")
    print(f"Average duration: {round(total_hours / completed_count, 2) if completed_count > 0 else 0}")
else:
    print(f"Error: {response.text}")
