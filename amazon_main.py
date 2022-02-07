import json
import firebase_admin
from firebase_admin import db

from a_scrape import Amazon_Scrape
from messaging import Messaging

text = '\u20b9'

# FireBase stuff
cred_obj = firebase_admin.credentials.Certificate('E:\PROJECTS\FIREBASE\\test\\test-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://test-project-5aa48-default-rtdb.asia-southeast1.firebasedatabase.app/'})

ref = db.reference("/")
best_sellers = ref.get()

for i in list(best_sellers.keys()):
    for j, k in enumerate(best_sellers[i]):
        amazon_scrape = Amazon_Scrape(k[0])
        data = f'''Book : {amazon_scrape.bookname}
        Author : {amazon_scrape.author}
        Price : Rs.{amazon_scrape.price.split(text)[1]}'''

        print(data)
        msg = Messaging()
        msg.send(msg_stuff=data)

        msg.email(body_text=data)

