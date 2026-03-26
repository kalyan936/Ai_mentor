import requests
import json
import time

base_url = "http://127.0.0.1:8002/api"

def test_health():
    print("Testing /health...")
    try:
        r = requests.get(f"http://127.0.0.1:8002/api/health")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_flow():
    email = f"test_{int(time.time())}@example.com"
    print(f"Testing flow for {email}...")
    
    # 1. Register
    reg_data = {"name": "Test User", "email": email}
    r = requests.post(f"{base_url}/users/register", json=reg_data)
    if r.status_code != 200:
        print(f"Register failed: {r.text}")
        return
    user = r.json()
    user_id = user["id"]
    print(f"Registered user ID: {user_id}")

    # 2. Roadmap
    print("Testing /roadmap/generate...")
    rd_data = {"user_id": user_id, "topic": "python", "current_level": "beginner"}
    r = requests.post(f"{base_url}/roadmap/generate", json=rd_data)
    print(f"Roadmap Status: {r.status_code}")
    print(f"Roadmap Response: {r.text[:200]}...")

    # 3. Lesson
    print("Testing /lessons/start...")
    params = {"user_id": user_id, "topic": "python", "subtopic": "syntax"}
    r = requests.post(f"{base_url}/lessons/start", params=params)
    print(f"Lesson Status: {r.status_code}")
    print(f"Lesson Response: {r.text[:200]}...")

if __name__ == "__main__":
    if test_health():
        test_flow()
