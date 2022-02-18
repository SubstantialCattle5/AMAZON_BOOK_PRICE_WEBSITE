import os
from typing import List, Any
from flask import *
import firebase_admin
from firebase_admin import db
from amazon_link_regex import Amazon_Link_Regex
from dotenv import load_dotenv  # pip install python-dotenv
import regex as re

load_dotenv("E:\PROJECTS\python\local_env\\amazon_book\\.env.txt")
app = Flask(__name__)

# Store book related stuff
book_names, max_book_prices = list(), list()
book_links = list()

# Password and Username variables
user_name = str()
password = str()

# FireBase stuff
cred_obj = firebase_admin.credentials.Certificate('E:\PROJECTS\FIREBASE\\test\\test-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': os.getenv('firebaseurl')})


# Extracting the book names from the link
def book_names_list(links):
    book_names_regex = Amazon_Link_Regex(link=links)
    book_names_regex.check()
    return book_names_regex.book_name


# Amazon JSON dump
def amazon_firebase_dump():
    data = dict()
    # To avoid passing empty list
    if len(book_links) != 0:
        # Creating a dict
        for i, (book_link, max_book_price) in enumerate(zip(book_links, max_book_prices)):
            data[i] = [book_link, max_book_price]
        # Uploading the data to firebase
        print(data)

        for i in data:
            # fixing 1 book data
            if len(data) == 1:
                ref = db.reference(f'{user_name}/{i}')
                ref.set(data[i])
                break
            else:
                ref = db.reference(f'/{user_name}/{i}')
                ref.set(data[i])


# --------------------------------------------HTML PAGES-------------------------------------------------------

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        global user_name, password
        # Save Button , passing value should not be zero
        if request.form.get('login') == 'Login' and len(request.form['User_name']) != 0 :
            user_name, password = request.form.get('User_name'), request.form.get('password')
            print(user_name)
            print(password)

            return redirect(url_for('main_pg'))
        else:
            return render_template('login_pg.html')
    else:
        return render_template('login_pg.html')


@app.route('/main', methods=["POST", "GET"])
def main_pg():
    global book_names, max_book_prices, book_links
    # POST is for buttons save and submit
    if request.method == 'POST':
        # Save Button , passing value should not be zero
        if request.form.get('save') == 'Save' and len(request.form['link_text']) != 0:
            book_names = book_names + [book_names_list(request.form['link_text'])]  # Creating the list
            max_book_prices = max_book_prices + [int(request.form['value']) * 10]  # Creating price list
            book_links.append(request.form['link_text'])
            return render_template('index.html', titles=book_names)

        elif request.form.get('Submit') == 'submit_':
            return redirect(url_for('confirmation_pg'))

        # Save button but length is equal to zero and acting as a clear button
        else:
            book_names, book_links, user_names = [], [], []
            return render_template('index.html')

    else:  # clearing the page
        book_names, book_links = [], []  # clearing the list
        return render_template('index.html')


@app.route('/confirmation', methods=['POST', 'GET'])
def confirmation_pg():
    if len(book_names) == 0:
        books = ['No books saved yet!']
    else:
        books = book_names
    # Confirm Button
    if request.method == 'POST':
        if request.form.get('save') == 'Save':
            if len(book_links) == 0 and len(max_book_prices) == 0:
                return render_template('confirmation.html', books=['ERROR! NO BOOKS SAVED'])
            else:
                amazon_firebase_dump()
                return render_template('confirmation.html', books=['Saved!'])

    else:
        return render_template('confirmation.html', books=book_names)


if __name__ == '__main__':
    app.run(debug=True)
