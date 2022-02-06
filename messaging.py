import smtplib
from twilio.rest import Client
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")


class Messaging:
    def __init__(self):
        self.account_sid = os.getenv('api')
        self.auth_token = os.getenv('token')
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, msg_stuff):
        message = self.client.messages.create(
            body=msg_stuff,
            from_=os.getenv('sphone'),
            to=os.getenv('phone'))
        print()
        print(message.status)

    def email(self, body_text):
        # Sender's email , subject  and body
        sender = os.getenv('remail')
        subject = 'Book Price Update'
        body = body_text
        email_service_smtp = 'smtp.gmail.com'
        myemail, mypassword = os.getenv('semail'), os.getenv('spw')
        with smtplib.SMTP(email_service_smtp) as connection:
            # Encrypting the mail contents
            connection.starttls()
            connection.login(user=myemail, password=mypassword)
            # sending the mail
            connection.sendmail(from_addr=myemail,
                                to_addrs=f'{sender}',
                                msg=f'Subject : {subject} \n\n {body} ')
