#!/usr/bin/env python3
"""
Test script for the complete booking flow:
1. Customer creates a booking request (without photographer)
2. Photographer views available requests
3. Photographer accepts the request
4. Verify the booking is assigned
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_booking_flow():
    print("🚀 Testing Complete Booking Flow")
    print("=" * 50)
    
    # Step 1: Create a customer booking request
    print("\n📝 Step 1: Creating customer booking request...")
    booking_data = {
        "customer_id": 2,  # Test customer ID
        "service_type": "wedding",
        "event_date": "2026-03-15",
        "event_time": "10:00 AM",
        "location": "Bangalore Palace",
        "notes": "Traditional wedding ceremony photography needed",
        "total_price": 25000
        # Note: photographer_id is omitted to create an open request
    }
    
    try:
        response = requests.post(f"{BASE_URL}/bookings", json=booking_data)
        if response.status_code == 201:
            booking = response.json()['booking']
            booking_id = booking['id']
            print(f"✅ Booking request created successfully! ID: {booking_id}")
            print(f"   Status: {booking['status']}")
            print(f"   Photographer ID: {booking['photographer_id']}")
        else:
            print(f"❌ Failed to create booking: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        return
    
    # Step 2: Get available booking requests (photographer view)
    print("\n🔍 Step 2: Fetching available booking requests...")
    try:
        response = requests.get(f"{BASE_URL}/bookings/requests")
        if response.status_code == 200:
            requests_data = response.json()['bookings']
            print(f"✅ Found {len(requests_data)} available requests")
            for req in requests_data:
                print(f"   - Request #{req['id']}: {req['service_type']} on {req['event_date']}")
        else:
            print(f"❌ Failed to get requests: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error fetching requests: {e}")
        return
    
    # Step 3: Photographer accepts the booking request
    print("\n🤝 Step 3: Photographer accepting booking request...")
    accept_data = {
        "photographer_id": 1  # Test photographer ID
    }
    
    try:
        response = requests.put(f"{BASE_URL}/bookings/{booking_id}/accept", json=accept_data)
        if response.status_code == 200:
            updated_booking = response.json()['booking']
            print(f"✅ Booking accepted successfully!")
            print(f"   Status: {updated_booking['status']}")
            print(f"   Photographer ID: {updated_booking['photographer_id']}")
        else:
            print(f"❌ Failed to accept booking: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error accepting booking: {e}")
        return
    
    # Step 4: Verify the booking is no longer in available requests
    print("\n✅ Step 4: Verifying booking is assigned...")
    try:
        response = requests.get(f"{BASE_URL}/bookings/requests")
        if response.status_code == 200:
            requests_data = response.json()['bookings']
            still_available = any(req['id'] == booking_id for req in requests_data)
            if not still_available:
                print("✅ Booking is no longer in available requests (correctly assigned)")
            else:
                print("❌ Booking still appears in available requests (incorrect)")
        
        # Check photographer's assigned bookings
        response = requests.get(f"{BASE_URL}/bookings/photographer/1")
        if response.status_code == 200:
            photographer_bookings = response.json()['bookings']
            assigned = any(b['id'] == booking_id for b in photographer_bookings)
            if assigned:
                print("✅ Booking appears in photographer's assigned bookings")
            else:
                print("❌ Booking not found in photographer's assigned bookings")
                
    except Exception as e:
        print(f"❌ Error verifying assignment: {e}")
    
    print("\n🎉 Booking flow test completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_booking_flow()
