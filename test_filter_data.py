#!/usr/bin/env python3
"""
Test script to check what data exists for each filter
"""
import requests
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = 'http://localhost:5000/api'

# Database config
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 5432)
}

def test_filters():
    print("=" * 70)
    print("TESTING ANALYTICS FILTERS")
    print("=" * 70)
    
    # Test each filter via API
    for filter_type in ['today', 'yesterday', 'week', 'month']:
        print(f"\n[{filter_type.upper()}]")
        try:
            response = requests.get(f'{API_BASE}/analytics/sessions?filter={filter_type}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"  Total Sessions: {data.get('total_sessions')}")
                print(f"  Active Sessions: {data.get('active_sessions')}")
                print(f"  Avg Duration: {data.get('average_duration')} hours")
            else:
                print(f"  ERROR: {response.status_code}")
        except Exception as e:
            print(f"  ERROR: {e}")

def check_database_dates():
    print("\n\n" + "=" * 70)
    print("CHECKING DATABASE DATES")
    print("=" * 70)
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get date range of data
        cursor.execute("""
            SELECT 
                MIN(DATE(check_in_time)) as earliest_date,
                MAX(DATE(check_in_time)) as latest_date,
                COUNT(*) as total_records
            FROM parking_history
        """)
        result = cursor.fetchone()
        
        print(f"\nData Range:")
        print(f"  Earliest: {result['earliest_date']}")
        print(f"  Latest: {result['latest_date']}")
        print(f"  Total Records: {result['total_records']}")
        
        # Get records by date
        cursor.execute("""
            SELECT 
                DATE(check_in_time) as date,
                COUNT(*) as count
            FROM parking_history
            GROUP BY DATE(check_in_time)
            ORDER BY date DESC
            LIMIT 10
        """)
        records = cursor.fetchall()
        
        print(f"\nRecords by Date (last 10 days):")
        for record in records:
            print(f"  {record['date']}: {record['count']} records")
        
        # Check today's date
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        print(f"\nToday's Date: {today}")
        print(f"Yesterday's Date: {yesterday}")
        
        # Check if we have data for today
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM parking_history
            WHERE DATE(check_in_time) = CURRENT_DATE
        """)
        today_count = cursor.fetchone()['count']
        print(f"Records for today: {today_count}")
        
        # Check if we have data for yesterday
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM parking_history
            WHERE DATE(check_in_time) = CURRENT_DATE - INTERVAL '1 day'
        """)
        yesterday_count = cursor.fetchone()['count']
        print(f"Records for yesterday: {yesterday_count}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_filters()
    check_database_dates()
