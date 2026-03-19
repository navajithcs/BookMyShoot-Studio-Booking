import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_flow():
    # 1. Register/Login Customer
    customer_email = "test_customer@example.com"
    customer_password = "Password123"
    
    print(f"Testing Customer Login: {customer_email}")
    response = requests.post(f"{BASE_URL}/login", json={
        "email": customer_email,
        "password": customer_password
    })
    
    if response.status_code != 200:
        print("Customer login failed. Attempting registration...")
        response = requests.post(f"{BASE_URL}/register", json={
            "first_name": "Test",
            "last_name": "Customer",
            "email": customer_email,
            "password": customer_password,
            "user_type": "customer"
        })
    
    if response.status_code not in [200, 201]:
        print(f"Customer Auth Failed: {response.text}")
        return

    customer_data = response.json()['user']
    customer_id = customer_data['id']
    print(f"Customer ID: {customer_id}")

    # 2. Login Photographer (to get ID)
    photographer_email = "photo@example.com"
    photographer_password = "Password123"
    
    print(f"Testing Photographer Login: {photographer_email}")
    response = requests.post(f"{BASE_URL}/login", json={
        "email": photographer_email,
        "password": photographer_password
    })
    
    if response.status_code != 200:
        print(f"Photographer Auth Failed: {response.text}")
        return

    photographer_data = response.json().get('user', {})
    print(f"Photographer User Data: {photographer_data}")
    
    photographer_id = photographer_data.get('photographer_id')
    if not photographer_id:
        print(f"ERROR: photographer_id missing in login response! Full response: {response.json()}")
        return
        
    print(f"Photographer ID: {photographer_id}")

    # 3. Create Booking
    print("Creating Booking...")
    booking_payload = {
        "customer_id": customer_id,
        "photographer_id": photographer_id,
        "service_type": "wedding",
        "event_date": "2026-12-31",
        "event_time": "10:00",
        "location": "Test Location",
        "notes": "Test Note",
        "total_price": 15000
    }
    
    response = requests.post(f"{BASE_URL}/bookings", json=booking_payload)
    if response.status_code != 201:
        print(f"Booking Creation Failed: {response.text}")
        return
    
    booking_data = response.json()['booking']
    booking_id = booking_data['id']
    print(f"Booking Created! ID: {booking_id}")

    # 4. Fetch Bookings for Photographer
    print(f"Fetching Bookings for Photographer ID {photographer_id}...")
    response = requests.get(f"{BASE_URL}/bookings/photographer/{photographer_id}")
    
    if response.status_code != 200:
        print(f"Fetch Failed: {response.text}")
        return
        
    bookings = response.json()['bookings']
    found = False
    for b in bookings:
        if b['id'] == booking_id:
            found = True
            print(f"SUCCESS: Found booking {booking_id} in photographer's list.")
            print(f"Status: {b['status']}")
            break
            
    if not found:
        print(f"ERROR: Booking {booking_id} NOT found in photographer's list.")
        print(f"Total bookings found: {len(bookings)}")

if __name__ == "__main__":
    test_flow()
