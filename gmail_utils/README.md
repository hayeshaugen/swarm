# gmail_utils

`gmail_utils` is a Python package that provides a simplified interface to interact with Gmail using the Gmail API. With this package, users can easily set up the Gmail service, list messages, retrieve message details, and send emails.

## Description

- **GmailService**: This class is responsible for setting up the Gmail service using provided credentials and token paths.
  
- **GmailClient**: This class provides methods to interact with Gmail, such as listing messages (with filtering options), retrieving a specific message, and sending an email.
  
- **EmailComposer**: A utility class to assist in creating email messages.

## Examples

### Setting up the Gmail Service

```python
from gmail_utils import GmailService

service = GmailService(credentials_path='path_to_client_secret.json', token_path='path_to_token.json')
```

### Listing Messages

```python
from gmail_utils import GmailClient

client = GmailClient(service.get_service())

# List all messages
messages = client.list_messages()
# Expected return: [{'id': 'some_id1', 'threadId': 'some_threadId1'}, {'id': 'some_id2', 'threadId': 'some_threadId2'}, ...]

# List only unread messages
unread_messages = client.list_messages(only_unread=True)
# Expected return: [{'id': 'some_id3', 'threadId': 'some_threadId3'}, ...]

# List a maximum of 5 messages
limited_messages = client.list_messages(max_results=5)
# Expected return: [{'id': 'some_id1', 'threadId': 'some_threadId1'}, ...] with a maximum of 5 entries.
```

### Sending a Message

```python
recipient = "example@email.com"
subject = "Hello from gmail_utils"
message_text = "This is a sample email sent using the gmail_utils package."

client.send_message(recipient, subject, message_text)
```
