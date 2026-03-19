#!/usr/bin/env python3
"""
Create test data for booking flow testing:
1. Create a test customer
2. Create a test photographer
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def create_test_users():
    print("👥 Creating Test Users")
    print("=" * 30)
    
    # Create test customer
    print("\n👤 Creating test customer...")
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "password123",
        "user_type": "customer",
        "phone": "9876543210"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=customer_data)
        if response.status_code == 201:
            customer = response.json()['user']
            print(f"✅ Customer created: {customer['email']} (ID: {customer['id']})")
            customer_id = customer['id']
        else:
            print(f"❌ Failed to create customer: {response.status_code}")
            if response.status_code == 400 and "already registered" in response.text:
                print("   Customer already exists, trying to get existing...")
                # Try to login to get existing customer
                login_data = {"email": "john.doe@test.com", "password": "password123"}
                login_response = requests.post(f"{BASE_URL}/login", json=login_data)
                if login_response.status_code == 200:
                    customer = login_response.json()['user']
                    customer_id = customer['id']
                    print(f"✅ Found existing customer: ID {customer_id}")
                else:
                    return None, None
            else:
                return None, None
    except Exception as e:
        print(f"❌ Error creating customer: {e}")
        return None, None
    
    # Create test photographer
    print("\n📸 Creating test photographer...")
    photographer_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@test.com",
        "password": "password123",
        "user_type": "photographer",
        "phone": "9876543211",
        "specialty": "Wedding Photography",
        "hourly_rate": 1500,
        "bio": "Professional wedding photographer with 5+ years experience"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=photographer_data)
        if response.status_code == 201:
            photographer = response.json()['user']
            photographer_id = photographer.get('photographer_id')
            print(f"✅ Photographer created: {photographer['email']} (ID: {photographer['id']}, Photographer ID: {photographer_id})")
        else:
            print(f"❌ Failed to create photographer: {response.status_code}")
            if response.status_code == 400 and "already registered" in response.text:
                print("   Photographer already exists, trying to get existing...")
                # Try to login to get existing photographer
                login_data = {"email": "jane.smith@test.com", "password": "password123"}
                login_response = requests.post(f"{BASE_URL}/login", json=login_data)
                if login_response.status_code == 200:
                    photographer = login_response.json()['user']
                    photographer_id = photographer.get('photographer_id')
                    print(f"✅ Found existing photographer: ID {photographer['id']}, Photographer ID {photographer_id}")
                else:
                    return customer_id, None
            else:
                return customer_id, None
    except Exception as e:
        print(f"❌ Error creating photographer: {e}")
        return customer_id, None
    
    print(f"\n🎉 Test users ready!")
    print(f"   Customer ID: {customer_id}")
    print(f"   Photographer ID: {photographer_id}")
    
    return customer_id, photographer_id

if __name__ == "__main__":
    create_test_users()
