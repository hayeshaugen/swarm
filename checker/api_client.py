import httpx 

class APIClientException(Exception):
    """Custom exception for API client errors."""

class APIClient:
    def __init__(self, config):
        self.config = config
        self.session = httpx.Client()
        
    def login(self, username, password):
        url = f"{self.config.BASE_URL}/login"
        headers = {
            "Content-Type": self.config.CONTENT_TYPE
        }
        body = {
            "username": username,
            "password": password
        }
        try:
            return self.session.post(url, headers=headers, data=body)
        except httpx.RequestError as exc:
            raise APIClientException(f"Error during login: {str(exc)}")
    
    def fetch_messages(self, session_cookie):
        url = f"{self.config.BASE_URL}/api/v1/messages"
        headers = {
            "Cookie": f"JSESSIONID={session_cookie}"
        }
        try:
            return self.session.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise APIClientException(f"Error fetching messages: {str(exc)}")
    
    def send_message(self, session_cookie, body):
        url = f"{self.config.BASE_URL}/api/v1/messages/"
        headers = {
            "Cookie": f"JSESSIONID={session_cookie}",
            "Content-Type": "application/json"
        }
        try:
            return self.session.post(url, headers=headers, json=body)
        except httpx.RequestError as exc:
            raise APIClientException(f"Error sending message: {str(exc)}")
    
    def close(self):
        self.session.close()
