import requests
import json

BASE_URL = "http://localhost:5000/api"

print("--- Testing Booking Flow ---")

booking_data = {
    "customer_id": 9,
    "service_type": "wedding",
    "event_date": "2026-03-15",
    "event_time": "10:00AM",
    "location": "Bangalore",
    "notes": "Looking for candid photography.",
    "total_price": 35000.0,
    "photographer_id": 2
}

print(f"Sending POST request to {BASE_URL}/bookings")
response = requests.post(f"{BASE_URL}/bookings", json=booking_data)

print(f"Response Code: {response.status_code}")
print(f"Raw Response: {response.text[:500]}")
