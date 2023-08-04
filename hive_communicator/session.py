from .api_client import APIClient
from .data_processor import DataProcessor

class Session:
    def __init__(self, config):
        self.api_client = APIClient(config)
        self.data_processor = DataProcessor()
    
    def login_to_service(self, username, password):
        response = self.api_client.login(username, password)
        print(f'1. response: {response}')
        return self._handle_response(response, expected_status=200, cookie_name="JSESSIONID")
    
    def fetch_messages(self, session_cookie):
        response = self.api_client.fetch_messages(session_cookie)
        return self._handle_response(response, expected_status=200)
    
    def send_message(self, session_cookie, device_id, user_application_id, data):
        encoded_data = self.data_processor.encode_data(data)
        body = {
            "deviceType": 1,  # Swarm M138 Modem
            "deviceId": self.data_processor.hex_to_int(device_id),
            "userApplicationId": user_application_id,
            "data": encoded_data
        }
        response = self.api_client.send_message(session_cookie, body)
        return self._handle_response(response, expected_status=200)
    
    def _handle_response(self, response, expected_status=200, cookie_name=None):
        if response.status_code == expected_status:
            if cookie_name:
                cookie_value = response.cookies.get(cookie_name)
                return {
                    "status": "success",
                    "cookie": cookie_value
                }
            else:
                return response.json()
        elif response.status_code in [401, 403]:
            return {"status": "error", "message": "Unauthorized or Forbidden"}
        else:
            return {"status": "error", "message": f"Unexpected status code {response.status_code}"}

    def close(self):
        self.api_client.close()
