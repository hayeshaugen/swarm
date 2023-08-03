import httpx
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

class Checker:
    def login_to_service(self, username, password):
            
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

    def fetch_messages(self, session_cookie):
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

    def hex_to_int(self, hex_value):
        return int(hex_value, 16)

    def send_message(self, session_cookie, device_id, user_application_id, data):

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
            "deviceId": self.hex_to_int(device_id),
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
