import requests
import base64
import json

def test_api():
    url = "http://127.0.0.1:5000/api/detect-mood"
    
    with open('face.jpg', 'rb') as f:
        pixel = base64.b64encode(f.read()).decode('utf-8')
        
    payload = {
        "image": "data:image/jpeg;base64," + pixel
    }
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
