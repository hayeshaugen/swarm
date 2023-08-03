import os
import base64
import email
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


class GmailClient:
    def __init__(self, credentials_path='./client_secret.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
        self.service = self._get_gmail_service()

    def _get_gmail_service(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def list_messages(self, query=''):
        response = self.service.users().messages().list(userId='me', q=query).execute()
        return response.get('messages', [])

    def get_message(self, message_id):
        message = self.service.users().messages().get(userId='me', id=message_id).execute()
        return message

    def send_message(self, to, subject, message_text):
        message = self.create_message(to, subject, message_text)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        body = {'raw': raw_message}
        self.service.users().messages().send(userId='me', body=body).execute()

    def create_message(self, to, subject, message_text):
        message = email.message.EmailMessage()
        message['to'] = to
        message['subject'] = subject
        message.set_content(message_text)
        return message

# Example usage
if __name__ == '__main__':
    gmail_client = GmailClient()

    # List messages
    messages = gmail_client.list_messages()
    print(f"Total messages: {len(messages)}")

    # Get and print a message
    if messages:
        message_id = messages[0]['id']
        message = gmail_client.get_message(message_id)
        print(json.dumps(message, indent=4))

    # Send a new message
    to_address = 'seventysevenllamas@gmail.com'
    subject = 'Test Email'
    message_text = 'This is a test email sent via the Gmail API.'
    gmail_client.send_message(to_address, subject, message_text)
    print("Message sent.")
