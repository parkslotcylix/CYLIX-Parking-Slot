#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 5432)
}

try:
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    print("Testing different date queries...")
    print("=" * 70)
    
    # Test 1: Get CURRENT_DATE
    cursor.execute("SELECT CURRENT_DATE")
    result = cursor.fetchone()
    print(f"\nCURRENT_DATE: {result}")
    
    # Test 2: Get a sample check_in_time
    cursor.execute("SELECT check_in_time FROM parking_history LIMIT 1")
    result = cursor.fetchone()
    print(f"\nSample check_in_time: {result}")
    
    # Test 3: Try different date extraction methods
    queries = [
        ("check_in_time::date", "SELECT check_in_time::date FROM parking_history LIMIT 1"),
        ("DATE(check_in_time)", "SELECT DATE(check_in_time) FROM parking_history LIMIT 1"),
        ("check_in_time::date = CURRENT_DATE", "SELECT COUNT(*) FROM parking_history WHERE check_in_time::date = CURRENT_DATE"),
        ("DATE(check_in_time) = CURRENT_DATE", "SELECT COUNT(*) FROM parking_history WHERE DATE(check_in_time) = CURRENT_DATE"),
    ]
    
    for name, query in queries:
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"\n{name}: SUCCESS")
            print(f"  Result: {result}")
        except Exception as e:
            print(f"\n{name}: ERROR")
            print(f"  {e}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Connection error: {e}")
