import json

from flask import Flask, render_template, request, redirect, url_for
import a_scrape
from amazon_link_regex import Amazon_Link_Regex

app = Flask(__name__)
link = str()
price = 0
book_names, max_book_prices = list(), list()
book_ = dict()
book_links = list()


# Extracting the book names from the link
def book_names_list(links):
    book_names_regex = Amazon_Link_Regex(link=links)
    book_names_regex.check()
    return book_names_regex.book_name


# Amazon JSON dump

def amazon_json_dump():
    data = dict()
    with open('amazon_book_links.json', 'w') as filehandle:
        for i, j in zip(book_links, max_book_prices):
            data[j] = i

        json.dump(data, filehandle, indent=4)


@app.route('/', methods=["POST", "GET"])
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

        # Save button but length is equal to zero
        else:
            book_names, book_links = [], []
            return render_template('index.html')

    else:  # clearing the page
        book_names, book_links = [], []
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
                return render_template('connfirmation.html', books=['ERROR! NO BOOKS SAVED'])
            else:
                amazon_json_dump()
                return render_template('confirmation.html', books=['Saved!'])

    elif request.method == 'GET':
        return render_template('confirmation.html', books=book_names)


if __name__ == '__main__':
    app.run(debug=True)
