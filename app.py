import os
import json
from hive_communicator import Session, Config
from gmail_utils import Client, Service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    hive_session = Session(Config())
    login_response = hive_session.login_to_service(username, password)
    print(login_response)
    session_cookie = login_response['cookie']

    device_id = os.getenv('DEVICEID')
    user_application_id = os.getenv('USERAPPID')
    data = 'Hello World from Space!'
    # send_message_response = send_message(session_cookie, device_id, user_application_id, data)
    # print(f'send message response: {send_message_response}')

    fetch_message_response = hive_session.fetch_messages(session_cookie)
    print(f'fetch message response: {fetch_message_response}')

    # List messages
    service = Service(credentials_path='client_secret.json', token_path='token.json')
    gmail_client = Client(service.get_service())
    messages = gmail_client.list_messages()
    print(f"Total messages: {len(messages)}")

    # Get and print a message
    if messages:
        message_id = messages[0]['id']
        message = gmail_client.get_message(message_id)
        print(json.dumps(message, indent=4))

if __name__ == '__main__':
    main()
