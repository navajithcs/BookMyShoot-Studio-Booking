#!/usr/bin/env python
"""Test the complete photographer display flow"""

import sys
sys.path.insert(0, 'backend')

import requests
import json
from datetime import datetime, timedelta
from app import app, db
from models import User, Photographer, Booking, Package

def test_photographer_display_flow():
    """Test that photographers are returned correctly for booking searches"""
    
    print("=" * 60)
    print("PHOTOGRAPHER DISPLAY FLOW TEST")
    print("=" * 60)
    
    # Test 1: Check photographers in database
    print("\n1. Checking photographers in database...")
    with app.app_context():
        photographers = Photographer.query.filter_by(is_available=True).all()
        print(f"   ✓ Found {len(photographers)} available photographers")
        
        for p in photographers:
            user_name = f"{p.user.first_name} {p.user.last_name}" if p.user else "Unknown"
            print(f"     - {user_name}: {p.specialty} ({p.location}) - ₹{p.hourly_rate}/hr")
    
    # Test 2: Test basic API endpoint
    print("\n2. Testing /api/photographers endpoint...")
    try:
        response = requests.get('http://localhost:5000/api/photographers')
        if response.status_code == 200:
            photographers = response.json().get('photographers', [])
            print(f"   ✓ API returned {len(photographers)} photographers")
        else:
            print(f"   ✗ API error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Connection error: {e}")
    
    # Test 3: Test search with different parameters
    print("\n3. Testing /api/photographers/search endpoint...")
    
    test_cases = [
        {'specialty': 'wedding', 'name': 'Wedding specialty'},
        {'specialty': 'birthday', 'name': 'Birthday specialty'},
        {'location': 'Kochi', 'name': 'Kochi location'},
        {'specialty': 'wedding', 'location': 'Kakkanad', 'name': 'Wedding + Kakkanad'},
        {}, # No filters
    ]
    
    for test_case in test_cases:
        params = test_case.copy()
        test_name = params.pop('name', 'Unknown')
        params['event_date'] = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        
        try:
            response = requests.get('http://localhost:5000/api/photographers/search', params=params)
            if response.status_code == 200:
                photographers = response.json().get('photographers', [])
                filters = ', '.join([f"{k}={v}" for k, v in params.items() if k != 'event_date'])
                print(f"   ✓ {test_name}: {len(photographers)} photographers ({filters})")
                
                if photographers:
                    p = photographers[0]
                    user_name = f"{p['user']['first_name']} {p['user']['last_name']}" if p.get('user') else "Unknown"
                    print(f"      Sample: {user_name} - {p['specialty']}")
            else:
                print(f"   ✗ {test_name}: API error {response.status_code}")
        except Exception as e:
            print(f"   ✗ {test_name}: {e}")
    
    # Test 4: Check if photographers have user info
    print("\n4. Checking photographer data structure...")
    try:
        response = requests.get('http://localhost:5000/api/photographers')
        if response.status_code == 200:
            photographers = response.json().get('photographers', [])
            if photographers:
                p = photographers[0]
                required_fields = ['id', 'specialty', 'location', 'hourly_rate', 'user', 'is_available']
                missing = [f for f in required_fields if f not in p]
                if missing:
                    print(f"   ✗ Missing fields: {missing}")
                else:
                    print(f"   ✓ All required fields present")
                    
                    if p.get('user'):
                        user_fields = ['first_name', 'last_name', 'email']
                        user_missing = [f for f in user_fields if f not in p['user']]
                        if user_missing:
                            print(f"   ✗ Missing user fields: {user_missing}")
                        else:
                            print(f"   ✓ User data complete")
    except Exception as e:
        print(f"   ✗ Error checking data: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
If all tests passed with ✓, then:
1. The database has photographers set up correctly
2. The API endpoints are working
3. The frontend should be able to display photographers

If photographers still don't show up in the browser:
1. Check the browser console for JavaScript errors (F12 DevTools)
2. Verify the frontend is using the correct API URL (http://localhost:5000/api)
3. Check that the customer is logged in before searching
4. Ensure all form fields (Date, Time, Duration) are filled in

NEXT STEPS FOR CUSTOMER:
1. Go to booking.html
2. Login if not already logged in
3. Select a package (e.g., Wedding)
4. Fill in: Event Date, Preferred Time, Duration
5. Click "🔍 Search Photographers"
6. Photographers should appear below!
    """)

if __name__ == '__main__':
    test_photographer_display_flow()
