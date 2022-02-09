import os
import firebase_admin
from firebase_admin import db
from dotenv import load_dotenv  # pip install python-dotenv

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

for i in list(best_sellers.keys()):
    for j, k in enumerate(best_sellers[i]):
        print(k)
        amazon_scrape = Amazon_Scrape(k[0])
        data = f'''Book : {amazon_scrape.bookname}
        Author : {amazon_scrape.author}
        Price : Rs.{amazon_scrape.price.split(text)[1]}'''
        print(data)
        msg = Messaging()
        msg.send(msg_stuff=data)

        msg.email(body_text=data)
