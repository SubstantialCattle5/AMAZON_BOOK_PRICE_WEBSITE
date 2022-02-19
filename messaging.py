import smtplib
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")



class Messaging:
    def __init__(self):
        self.account_sid = os.getenv('api')
        self.auth_token = os.getenv('token')

    def email(self, body_data):
        # Sender's email , subject  and body

        emails = list(body_data.keys())
        for email in emails:
            sending = str()
            for data in (body_data[email]):
                price = float(data['Price'][2:len(data['Price'])])
                if price <= float(data['Decided Price']) or price >= float(
                        data['Decided Price']):  # NOTE : REMOVE THE SECOND PART
                    send = f"""\n\nName : {data['Name']}\nToday's Price : Rs.{float(data['Price'][2:len(data['Price'])])}\nDecided Price: Rs.{data['Decided Price']}\nLink : {data['link']}"""
                    sending = sending + send

            print(sending)

            sender = os.getenv('remail')
            subject = 'Book Price Update'
            body = body_data
            email_service_smtp = 'smtp.gmail.com'
            myemail, mypassword = os.getenv('semail'), os.getenv('spw')
            with smtplib.SMTP(email_service_smtp) as connection:
                # Encrypting the mail contents
                connection.starttls()
                connection.login(user=myemail, password=mypassword)
                # sending the mail
                connection.sendmail(from_addr=myemail,
                                    to_addrs=f'{email}',
                                    msg=f'Subject : {subject} \n\n {sending} ')




