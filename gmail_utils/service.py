import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

class GmailService:
    def __init__(self, credentials_path='client_secret.json', token_path='token.json', scopes=None):
        self._credentials_path = credentials_path
        self._token_path = token_path
        self._scopes = scopes or ['https://www.googleapis.com/auth/gmail.readonly',
                                  'https://www.googleapis.com/auth/gmail.send']
        self._service = self._get_gmail_service()

    def _get_gmail_service(self):
        creds = None
        if os.path.exists(self._token_path):
            creds = Credentials.from_authorized_user_file(self._token_path, self._scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self._credentials_path, self._scopes)
                flow.redirect_uri = 'http://localhost:8080/'
                creds = flow.run_local_server(port=8080)
            with open(self._token_path, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def get_service(self):
        return self._service
