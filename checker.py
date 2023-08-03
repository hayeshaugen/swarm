import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def login_to_service():
    # Get the username and password from the environment variables
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
    with httpx.Client() as client:
        response = client.post(url, headers=headers, data=body)
    
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

def fetch_messages(session_cookie):
    url = "https://bumblebee.hive.swarm.space/hive/api/v1/messages"
    headers = {
        "Cookie": f"JSESSIONID={session_cookie}"
    }
    
    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        
    if response.status_code == 200:
        return response.json()
    elif response.status_code in [401, 403]:
        return {"status": "error", "message": "Unauthorized or Forbidden"}
    else:
        return {"status": "error", "message": f"Unexpected status code {response.status_code}"}

# Test
login_response = login_to_service()
session_cookie = login_response['cookie']
messages = fetch_messages(session_cookie)

print(messages)
