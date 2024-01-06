from django.core.mail import EmailMessage,get_connection
import os

class Util:
   
    @staticmethod
    def sent_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']],
            connection=get_connection(),
        )
        email.send()