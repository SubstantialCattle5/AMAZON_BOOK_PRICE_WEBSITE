import regex as re


class Amazon_Link_Regex:
    def __init__(self, link):
        self.link = link
        self.book_name = str()


    def check(self):
        if re.search('^https://www.amazon.in/', self.link):
            book_name_list = self.link.split('/')[3].split('-')  # Taking out the name of the book
            for i in book_name_list:  # converting the list to string
                self.book_name = self.book_name + ' ' + i
            self.book_name = self.book_name[1:len(self.book_name)]  # To remove the initial space



