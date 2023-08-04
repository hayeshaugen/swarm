from email.message import EmailMessage

class EmailComposer:
    @staticmethod
    def create_message(to, subject, message_text):
        message = EmailMessage()
        message['to'] = to
        message['subject'] = subject
        message.set_content(message_text)
        return message
