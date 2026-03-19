import requests
import sys

BASE_URL = "http://localhost:5000/api"

def test_login(email, password):
    print(f"Attempting login for: {email} with password: {password}")
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            "email": email,
            "password": password
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("LOGIN SUCCESS")
            return True
        else:
            print("LOGIN FAILED")
            return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Admin Login (New Admin)
    print("--- Test 1: Admin Login ---")
    test_login("new_admin@bookmyshoot.com", "NewAdmin123")
    
    # Test 2: Standard Admin Login (Reset)
    print("\n--- Test 2: Reset Admin Login ---")
    test_login("admin@bookmyshoot.com", "Admin123")

    # Test 3: Random/Invalid Login
    print("\n--- Test 3: Invalid Login ---")
    test_login("fake@user.com", "wrongpass")
