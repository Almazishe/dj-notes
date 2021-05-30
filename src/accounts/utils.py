from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data.get('email_subject'),
            body=data.get('email_body'),
            to=[data.get('to_email')]
        )
        email.send()

