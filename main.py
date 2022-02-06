from flask import Flask, render_template, request
import a_scrape
import messaging

app = Flask(__name__)
link = str()
price = 0
book_names, book_prices = [], list()


def amazon(url_link: str):
    global book_names, book_prices
    amazon_data = a_scrape.Amazon_Scrape(url=url_link)
    book_names.append(amazon_data.bookname)
    book_prices.append(amazon_data.price)


@app.route('/', methods=["POST", "GET"])
def main_pg():
    global book_names
    if request.method == 'POST' :
        if request.form.get('save') == 'Save' and len(request.form['link_text']) != 0:
            link, price = request.form['link_text'], request.form['value']
            amazon(url_link=f'{link}')
            print('hello')
            return render_template('index.html', titles=book_names)
        elif request.form.get('Submit') == 'submit_':
            print('save')
            return render_template('index.html')
    else:
        book_names = []
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
