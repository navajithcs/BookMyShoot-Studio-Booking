
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_cancel(booking_id, photographer_id):
    url = f"{BASE_URL}/bookings/{booking_id}/photographer-cancel"
    data = {"photographer_id": photographer_id, "reason": "Test cancellation"}
    print(f"Calling PUT: {url}")
    print(f"Data: {data}")
    try:
        response = requests.put(url, json=data)
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response Body (non-JSON): {response.text[:500]}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    # Test with booking 41 and photographer 3
    test_cancel(41, 3)
