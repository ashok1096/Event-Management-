import json
import urllib.request

def test_login():
    url = "http://localhost:8000/auth/login"
    payload = json.dumps({
        "email": "ashok@gmail.com",
        "password": "admin"
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Status:", response.status)
            print("Response:", response.read().decode('utf-8'))
    except Exception as e:
        print("Error:", e)
        if hasattr(e, 'read'):
            print("Response:", e.read().decode('utf-8'))

if __name__ == "__main__":
    test_login()
