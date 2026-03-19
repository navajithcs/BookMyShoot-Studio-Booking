
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_check(booking_id, photographer_id):
    url = f"{BASE_URL}/bookings/{booking_id}/cancellation-check?photographer_id={photographer_id}"
    print(f"Calling: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response Body (non-JSON): {response.text[:500]}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_check(41, 3)
