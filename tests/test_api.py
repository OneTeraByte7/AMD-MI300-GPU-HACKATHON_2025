import requests
import time

# Replace with your actual test data
payload = {
    "Request_id": "123",
    "From": "userone@example.com",
    "Attendees": [{"email": "usertwo@example.com"}],
    "Duration_mins": 30,
    "start_window": "2025-07-13T10:00:00+05:30",
    "end_window": "2025-07-13T18:00:00+05:30",
    "timezone": "Asia/Kolkata"
}

# Send meeting request
response = requests.post("http://127.0.0.1:5000/receive", json=payload)
print("POST /receive response:", response.json())

job_id = response.json().get("job_id")
if not job_id:
    print("No job_id returned!")
    exit(1)

# Poll for result
for _ in range(10):
    result = requests.get(f"http://127.0.0.1:5000/result/{job_id}")
    res_json = result.json()
    print("GET /result response:", res_json)
    if res_json.get("status") != "running":
        if "error" in res_json:
            print("Error from backend:", res_json["error"])
        break
    time.sleep(2)