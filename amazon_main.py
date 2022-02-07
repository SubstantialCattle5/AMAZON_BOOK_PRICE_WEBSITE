import json

from  a_scrape import Amazon_Scrape
from messaging import Messaging

text = '\u20b9'


with open('amazon_book_links.json' , 'r' ) as filehandle :
    file = json.load(filehandle)
    costs = list(file.keys())
    links = list(file.values())

    for i in links :
            amazon_scrape = Amazon_Scrape(i)
            data = f'''Book : {amazon_scrape.bookname}
            Author : {amazon_scrape.author}
            Price : Rs.{amazon_scrape.price.split(text)[1]}'''
            print(data)
            msg = Messaging()
            msg.send(msg_stuff=data)

            msg.email(body_text=data)









