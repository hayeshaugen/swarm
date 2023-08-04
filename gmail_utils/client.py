import base64
from .composer import EmailComposer

class Client:
    def __init__(self, service):
        self._service = service

    def list_messages(self, query='', max_results=None, only_unread=False):
        if only_unread:
            query = f"{query} is:unread"
        response = self._service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return response.get('messages', [])

    def get_message(self, message_id):
        message = self._service.users().messages().get(userId='me', id=message_id).execute()
        return message

    def send_message(self, to, subject, message_text):
        message = EmailComposer.create_message(to, subject, message_text)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        body = {'raw': raw_message}
        self._service.users().messages().send(userId='me', body=body).execute()

