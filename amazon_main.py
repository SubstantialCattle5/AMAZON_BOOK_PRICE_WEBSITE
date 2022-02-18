import os
import firebase_admin
from firebase_admin import db
from dotenv import load_dotenv  # pip install python-dotenv
import prettytable

load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")
from a_scrape import Amazon_Scrape
from messaging import Messaging

text = '\u20b9'

# FireBase stuff
cred_obj = firebase_admin.credentials.Certificate('E:\PROJECTS\FIREBASE\\test\\test-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': os.getenv('firebaseurl')})

ref = db.reference("/")
best_sellers = ref.get()

# Pretty Table
x = prettytable.PrettyTable()
x.field_names = ["Book Name", "Author", "Cost"]

try:
    for i in list(best_sellers.keys()):
        for j, k in enumerate(best_sellers[i]):
            amazon_scrape = Amazon_Scrape(k[0])
            try:
                x.add_row([amazon_scrape.bookname, amazon_scrape.author, f'Rs.{amazon_scrape.price.split(text)[1]}'])
            except IndexError:
                print('error')

# if the database doesn't has any saved books
except AttributeError:
    print('No Saved Book!!!')

# Emailing the user
print(x)
msg = Messaging()
msg.email(body_text=x)
