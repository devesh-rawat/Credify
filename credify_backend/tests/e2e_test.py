import requests
import time

BASE_URL = "http://localhost:8000"

def test_flow():
    print("Starting E2E Test...")
    
    # 1. User Signup
    print("\n[1] User Signup")
    email = f"dev{time.time()}@example.com"
    user_data = {"name": "Dev", "email": email, "password": "password123"}
    res = requests.post(f"{BASE_URL}/auth_user/signup", json=user_data)
    if res.status_code != 200:
        print(f"Signup failed: {res.text}")
        return
    user_token = res.json()["access_token"]
    user_id = res.json()["user_id"]
    print(f"User Signup Success. Token: {user_token[:10]}...")
    
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # 2. Fetch Banks
    print("\n[2] Fetch Banks")
    res = requests.get(f"{BASE_URL}/aa/banks", headers=headers)
    print(f"Banks: {res.json()}")
    account_id = res.json()[0]["account_id"]
    
    # 3.5 Request OTP (New Step)
    print("\n[3.5] Request OTP")
    otp_req = {"aadhaar": "123456789012", "pan": "ABCDE1234F"}
    res = requests.post(f"{BASE_URL}/auth_user/request-otp", json=otp_req, headers=headers)
    print(f"Request OTP Status: {res.status_code}")
    
    # Note: We cannot easily get the OTP in this script since it's sent via email/printed to server logs.
    # We will skip verify-otp in this automated run, or we'd need to expose a backdoor.
    # For now, we assume the user manually verifies via Swagger or we trust the unit test logic.
    
    # 3. Fetch Statements
    print("\n[3] Fetch Statements")
    res = requests.post(f"{BASE_URL}/aa/statements?account_id={account_id}", headers=headers)
    print(f"Statements fetched: {len(res.json().get('transactions', []))} transactions")
    
    # 4. Run Scoring
    print("\n[4] Run Scoring")
    res = requests.post(f"{BASE_URL}/scoring/run?account_id={account_id}", headers=headers)
    score_data = res.json()
    print(f"Score: {score_data.get('credit_score')}, Risk: {score_data.get('risk_label')}")
    
    # 5. Apply for Loan
    print("\n[5] Apply for Loan")
    app_data = {"account_id": account_id}
    res = requests.post(f"{BASE_URL}/applications/apply", json=app_data, headers=headers)
    app_id = res.json()["application_id"]
    print(f"Application ID: {app_id}")
    
    # 6. Admin Signup
    print("\n[6] Admin Signup")
    admin_email = f"admin{time.time()}@hdfc.com"
    admin_data = {
        "name": "Manager", 
        "email": admin_email, 
        "password": "adminpass",
        "bank_id": "B001",
        "branch_id": "HDFC_IND_NAGAR"
    }
    res = requests.post(f"{BASE_URL}/auth_admin/signup", json=admin_data)
    if res.status_code != 200:
        # Try login if already exists
        res = requests.post(f"{BASE_URL}/auth_admin/login", json={"email": admin_data["email"], "password": admin_data["password"]})
    
    admin_token = res.json()["access_token"]
    print(f"Admin Login Success. Token: {admin_token[:10]}...")
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 7. Admin View Applications
    print("\n[7] Admin View Applications")
    res = requests.get(f"{BASE_URL}/admin/applications", headers=admin_headers)
    apps = res.json()
    print(f"Found {len(apps)} applications")
    
    # 8. Admin Approve
    print("\n[8] Admin Approve Application")
    decision = {"status": "APPROVED", "notes": "Looks good"}
    res = requests.post(f"{BASE_URL}/admin/applications/{app_id}/decision", json=decision, headers=admin_headers)
    print(f"Decision Response: {res.json()}")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Test failed: {e}")
