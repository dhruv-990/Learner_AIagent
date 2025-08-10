#!/usr/bin/env python3
"""Test authentication flow with fixes"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("Testing authentication flow with fixes...")

    # Test 1: Register a new user
    print("\n1. Testing user registration...")
    register_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/register", json=register_data)
        print(f"Register response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Registration successful")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

    # Test 2: Login
    print("\n2. Testing user login...")
    login_data = {
        "username": "testuser2",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("✅ Login successful, got token")
                print(f"Token: {token[:50]}...")
            else:
                print("❌ No token in response")
                return False
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

    # Test 3: Create a learning path (this should work now)
    print("\n3. Testing learning path creation...")
    headers = {"Authorization": f"Bearer {token}"}
    learning_path_data = {
        "topic": "Python Programming",
        "experience_level": "beginner",
        "time_commitment": "5-10 hours per week",
        "learning_goals": "Learn Python basics and build simple projects"
    }

    try:
        response = requests.post(f"{BASE_URL}/create-learning-path", json=learning_path_data, headers=headers)
        print(f"Learning path creation response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Learning path creation successful!")
            result = response.json()
            if result.get("success"):
                print("✅ API returned success")
            else:
                print(f"⚠️ API returned: {result}")
        else:
            print(f"❌ Learning path creation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Learning path creation error: {e}")
        return False

    # Test 4: Check if users.json file was created
    print("\n4. Checking user persistence...")
    try:
        import os
        if os.path.exists("users.json"):
            print("✅ users.json file exists")
            with open("users.json", "r") as f:
                users_data = json.load(f)
                print(f"✅ Found {len(users_data)} users in file")
                if "testuser2" in users_data:
                    print("✅ Our test user is saved in the file")
                else:
                    print("❌ Test user not found in file")
                    return False
        else:
            print("❌ users.json file not found")
            return False
    except Exception as e:
        print(f"❌ Error checking user file: {e}")
        return False

    print("\n🎉 All tests passed! Both issues are fixed!")
    return True

if __name__ == "__main__":
    test_auth_flow() 