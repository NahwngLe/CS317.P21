import requests
import time
import random

url = "http://localhost:8000/predict"

payload_template = {
    "feature": [
        123456, 10, 8, 500, 400, 60, 40, 50.0, 7.07, 55, 35, 45.0, 7.07,
        9000.0, 5.0, 1000.0, 100.0, 2000, 500, 5000, 1000.0, 200.0, 1500, 500,
        4000, 800.0, 150.0, 1200, 400, 0, 0, 0, 0, 120, 100, 2.0, 1.5, 35, 65,
        50.0, 10.0, 100.0, 0, 1, 0, 0, 1, 0, 0, 0, 1.2, 52.0, 50.0, 45.0, 120,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 500, 8, 400, 256, 256, 1, 20,
        3000.0, 400.0, 4000, 2000, 10000.0, 500.0, 11000, 9000
    ]
}

for i in range(1000):
    try:
        payload = payload_template.copy()
        payload["feature"][0] = random.randint(100000, 999999)

        response = requests.post(url, json=payload)
        print(f"[{i}] Status: {response.status_code}")
    except Exception as e:
        print(f"[{i}] Error: {e}")

    time.sleep(random.uniform(0.01, 0.3))
