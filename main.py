import json
from flask import *
import firebase_admin
from firebase_admin import db
from amazon_link_regex import Amazon_Link_Regex

app = Flask(__name__)
link = str()
price = 0
book_names, max_book_prices, user_names = list(), list(), list()
book_ = dict()
book_links = list()

# FireBase stuff
cred_obj = firebase_admin.credentials.Certificate('E:\PROJECTS\FIREBASE\\test\\test-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://test-project-5aa48-default-rtdb.asia-southeast1.firebasedatabase.app/'})


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
        for book_link, max_book_price, user_name in zip(book_links, max_book_prices, user_names):
            data[user_name] = [book_link, max_book_price]
        # Uploading the data to firebase
        print(data)
        for i in data:
            ref = db.reference(f"/{i}")
            ref.set(data[i])


@app.route('/', methods=["POST", "GET"])
def main_pg():
    global book_names, max_book_prices, book_links, user_names
    # POST is for buttons save and submit
    if request.method == 'POST':
        # Save Button , passing value should not be zero
        if request.form.get('save') == 'Save' and len(request.form['link_text']) != 0:
            user_names = user_names + [request.form['User_name']]
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
            if len(book_links) == 0 and len(max_book_prices) == 0 and len(user_names) == 0:
                return render_template('confirmation.html', books=['ERROR! NO BOOKS SAVED'])
            else:
                amazon_firebase_dump()
                return render_template('confirmation.html', books=['Saved!'])

    else:
        return render_template('confirmation.html', books=book_names)


if __name__ == '__main__':
    app.run(debug=True)
