import requests
import os
from dotenv import load_dotenv

load_dotenv()

def login_to_service():
    # Get the login credentials
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    # Define the endpoint
    url = "https://bumblebee.hive.swarm.space/hive/login"
    
    # Define the headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Define the request body
    body = {
        "username": username,
        "password": password
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, data=body)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the cookie value from the response headers
        cookie_value = response.cookies.get("JSESSIONID")
        return {
            "status": "success",
            "cookie": cookie_value
        }
    elif response.status_code == 401:
        return {
            "status": "failed",
            "message": "Unauthorized"
        }
    else:
        return {
            "status": "error",
            "message": f"Unexpected status code {response.status_code}"
        }

# Test
result = login_to_service()
print(result)

