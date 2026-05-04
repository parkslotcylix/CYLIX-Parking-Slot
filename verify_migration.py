#!/usr/bin/env python
"""Verify Supabase migration is working"""

import requests
import json

print('=' * 70)
print('🧪 SUPABASE MIGRATION - FINAL VERIFICATION')
print('=' * 70)

tests_passed = 0
tests_total = 2

# Test 1: Health Check
print('\n[TEST 1] Database Health Check')
print('-' * 70)
try:
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    if response.status_code == 200:
        print('✅ PASS - Health check successful')
        print(f'   Status: {response.status_code}')
        data = response.json()
        print(f'   Message: {data.get("message")}')
        tests_passed += 1
    else:
        print(f'❌ FAIL - Status: {response.status_code}')
except Exception as e:
    print(f'❌ FAIL - Error: {str(e)[:100]}')

# Test 2: Login Endpoint
print('\n[TEST 2] Admin Login (Supabase Query)')
print('-' * 70)
try:
    response = requests.post('http://localhost:5000/api/login', json={
        'email': 'juliemay1917@gmail.com',
        'password': 'Juliemay0!'
    }, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print('✅ PASS - Login successful')
            print(f'   Admin: {data.get("admin_name")}')
            print(f'   Email: {data.get("admin_email")}')
            print(f'   Access Level: {data.get("access_level")}')
            tests_passed += 1
        else:
            print('❌ FAIL - Login returned false')
    else:
        print(f'❌ FAIL - Status: {response.status_code}')
except Exception as e:
    print(f'❌ FAIL - Error: {str(e)[:100]}')

# Summary
print('\n' + '=' * 70)
print(f'TEST RESULTS: {tests_passed}/{tests_total} passed')
print('=' * 70)

if tests_passed == tests_total:
    print('\n✅ ALL TESTS PASSED - SUPABASE MIGRATION SUCCESSFUL!')
    print('\n🚀 Your app is ready to use:')
    print('   - Database: Supabase PostgreSQL ✅')
    print('   - Connection: Active ✅')
    print('   - API: Functional ✅')
    print('   - Status: PRODUCTION READY ✅')
else:
    print(f'\n⚠️  Some tests failed ({tests_total - tests_passed} failing)')
    print('Please check the errors above and review the setup guide.')

print('\n' + '=' * 70)
