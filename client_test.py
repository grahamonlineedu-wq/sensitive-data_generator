import requests

url = "http://127.0.0.1:5000/api/dual-agent-fetch"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer fake-token"
}
payload = {
    "user_id": "user_001",
    "official_clearance_code": "SECURE-KEY-2026",
    "purpose": "Official Emergency Audit"
}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())

