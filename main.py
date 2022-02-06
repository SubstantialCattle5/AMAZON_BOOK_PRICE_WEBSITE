from flask import Flask, render_template, request
import a_scrape
import messaging

app = Flask(__name__)
link = str()
price = 0


def amazon(url_link: str):
    amazon_data = a_scrape.Amazon_Scrape(url=url_link)
    print(amazon_data.bookname)


@app.route('/', methods=["POST", "GET"])
def main_pg():
    if request.method == 'POST':
        link, price = request.form['link_text'], request.form['value']
        amazon(url_link=f'{link}')
        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
