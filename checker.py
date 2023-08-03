import httpx
import os
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

def login_to_service(username, password):
        
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

def hex_to_int(hex_value):
    return int(hex_value, 16)

def send_message(session_cookie, device_id, user_application_id, data):
    url = "https://bumblebee.hive.swarm.space/hive/api/v1/messages/"
    headers = {
        "Cookie": f"JSESSIONID={session_cookie}",
        "Content-Type": "application/json"
    }
    
    # Base64 encode the data
    encoded_data = base64.b64encode(data.encode()).decode()
    
    # Prepare the body of the request
    body = {
        "deviceType": 1,  # Swarm M138 Modem
        "deviceId": hex_to_int(device_id),
        "userApplicationId": user_application_id,
        "data": encoded_data
    }

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=body)
        
    if response.status_code == 200:
        return response.json()
    elif response.status_code in [401, 403]:
        return {"status": "error", "message": "Unauthorized or Forbidden"}
    else:
        return {"status": "error", "message": f"Unexpected status code {response.status_code}"}


# Test
#
# Get the username and password from the environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
login_response = login_to_service(username, password)
print(f'login response: {login_response}')

session_cookie = login_response['cookie']

device_id = os.getenv('DEVICEID')
print(f'device id as int: {hex_to_int(device_id)}')
user_application_id = os.getenv('ORGID')
data = 'Hello World from Space!'
send_message_response = send_message(session_cookie, device_id, user_application_id, data)
print(f'send message response: {send_message_response}')

fetch_message_response = fetch_messages(session_cookie)
print(f'fetch message response: {fetch_message_response}')


