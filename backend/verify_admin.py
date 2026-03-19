import requests

BASE_URL = "http://localhost:5000/api"

def verify_admin():
    print("Testing Admin Login...")
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "admin@bookmyshoot.com",
        "password": "Admin123"
    })
    
    if response.status_code != 200:
        print(f"Login Failed: {response.text}")
        return

    data = response.json()
    user = data['user']
    print(f"Login Success! User Type: {user['user_type']}")
    
    if user['user_type'] != 'admin':
        print("ERROR: User is not admin!")
        return

    print("\nTesting Admin Stats API...")
    response = requests.get(f"{BASE_URL}/admin/stats")
    
    if response.status_code != 200:
        print(f"Stats API Failed: {response.text}")
        return
        
    stats = response.json()
    print("Stats Retrieved Successfully:")
    print(f"Revenue: ₹{stats['revenue']['total']}")
    print(f"Total Users: {stats['users']['total']}")
    print(f"Active Bookings: {stats['bookings']['pending'] + stats['bookings']['accepted']}")

if __name__ == "__main__":
    verify_admin()
