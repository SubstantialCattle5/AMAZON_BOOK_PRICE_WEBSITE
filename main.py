from flask import Flask, render_template, request
import a_scrape
from amazon_link_regex import Amazon_Link_Regex

app = Flask(__name__)
link = str()
price = 0
book_names, max_book_prices = [], []


# Extracting the book names from the link
def book_names_list(links):
    book_names_regex = Amazon_Link_Regex(link=links)
    book_names_regex.check()
    return book_names_regex.book_name


@app.route('/', methods=["POST", "GET"])
def main_pg():
    global book_names , max_book_prices
    # POST is for buttons save and submit
    if request.method == 'POST':
        # Save Button , passing value should not be zero
        if request.form.get('save') == 'Save' and len(request.form['link_text']) != 0:
            link, price = request.form['link_text'], request.form['value']
            book_names = book_names + [book_names_list(link)] # Creating the list
            max_book_prices = max_book_prices + [int(price)*10]
            print(max_book_prices, type(int(price)))

            return render_template('index.html', titles=book_names)

        # Submit button
        elif request.form.get('Submit') == 'submit_':
            return render_template('index.html')

        # Save button but length is not equal to zero
        else:
            return render_template('index.html')

    else:  # clearing the page
        book_names = []
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
