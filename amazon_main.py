import os
import firebase_admin
from firebase_admin import db
from dotenv import load_dotenv
load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")
from a_scrape import Amazon_Scrape


text = '\u20b9'

# FireBase stuff
cred_obj = firebase_admin.credentials.Certificate('E:\PROJECTS\FIREBASE\\test\\test-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': os.getenv('firebaseurl')})

ref = db.reference("/")
best_sellers = ref.get()

data, book_names = dict(), list()
try:
    for best_seller in list(best_sellers.keys()):
        email = best_sellers[best_seller]['email']
        check = 0
        for link in best_sellers[best_seller]['data']:
            if check == 0:
                book_names = list()
            amazon = Amazon_Scrape(link[0])
            amazon_book_data = {'Name': amazon.bookname, 'Price': amazon.price, 'Decided Price': link[1] , 'link' : link[0]}
            book_names.append(amazon_book_data)
            check+=1
        data[email] = book_names

        # if the database doesn't have any saved books
except AttributeError:
    print('No Saved Book!!!')

# Emailing the user
print(data)
