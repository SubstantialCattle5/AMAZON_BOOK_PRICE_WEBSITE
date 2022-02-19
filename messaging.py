import smtplib
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")

a = {'samless123@rediffmail.com': [
    {'Name': ' Charlie and the Great Glass Elevator ', 'Price': ' ₹287.00 ', 'Decided Price': 100,
     'link': 'https://www.amazon.in/Charlie-Great-Glass-Elevator-Fiction/dp/0141365382/ref=sr_1_1?keywords=roald+dahl+books&qid=1644111339&sprefix=roald+%2Caps%2C248&sr=8-1'}],
    'samless274@gmail.com': [{'Name': ' 1984 ', 'Price': ' ₹154.00 ', 'Decided Price': 100,
                              'link': 'https://www.amazon.in/1984-George-Orwell/dp/8192910903/ref=sr_1_3?crid=27SRFVXEKR4OX&keywords=1984&qid=1644108531&sprefix=1984%2Caps%2C258&sr=8-3'},
                             {'Name': ' Animal Farm ', 'Price': ' ₹70.00 ', 'Decided Price': 100,
                              'link': 'https://www.amazon.in/Animal-Farm-George-Orwell/dp/812911612X/ref=sr_1_3?crid=3UNXI00VXNY5O&keywords=animal+farm&qid=1644112139&sprefix=animal+farm%2Caps%2C260&sr=8-3'}]}


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
                                    to_addrs=f'{sender}',
                                    msg=f'Subject : {subject} \n\n {sending} ')



ab = Messaging()
ab.email(a)
