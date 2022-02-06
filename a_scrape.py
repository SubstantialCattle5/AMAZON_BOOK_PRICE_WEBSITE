from bs4 import BeautifulSoup
import requests


class Amazon_Scrape:
    def __init__(self , url):
        self.url = url
        self.data = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/97.0.4692.71 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9'}
        self.link = requests.get(url=self.url, headers=self.data)
        self.soup = BeautifulSoup(self.link.text, 'lxml')
        self.bookname, self.price, self.author = str(), str(), str()

        self.search()

    def search(self):
        # Returns the name of the book
        self.bookname = self.soup.find(name='span', id="productTitle", class_='a-size-extra-large').getText()
        # Author
        self.author = self.soup.find(name='a', class_='a-link-normal contributorNameID').getText()
        # Returns the price of the book
        self.price = self.soup.find(name='span', class_="a-size-base a-color-price a-color-price").getText()
