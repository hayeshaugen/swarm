import requests

while True:
    response = requests.post("http://www.example.com")
    if response.status_code == 200:
        print("POST request successful")
    else:
        print(f"POST request failed with status code: {response.status_code}")
