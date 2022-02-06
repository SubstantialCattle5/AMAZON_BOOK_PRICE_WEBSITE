from flask import Flask, render_template, request

app = Flask(__name__)
link = str()
price = 0


@app.route('/', methods=["POST", "GET"])
def main_pg():
    if request.method == 'POST':
        global link, price
        link, price = request.form['link_text'], request.form['value']
        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
