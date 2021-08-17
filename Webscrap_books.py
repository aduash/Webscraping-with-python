import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import sqlite3

no_pages = 2

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('Books_rating.sqlite')
cur = conn.cursor()

# create tables
cur.executescript('''
DROP TABLE IF EXISTS Books;

CREATE TABLE Books(
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Book_name   TEXT,
    Author TEXT,
    Rating FLOAT,
    Customers_rated INTEGER,
    Price FLOAT
);
''')


def get_data(page_no):
    url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_' + str(page_no) + '?ie=UTF8&pg=' + str(page_no)
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    #alls = []
    for d in soup.findAll('div', attrs={'class': 'a-section a-spacing-none aok-relative'}):
        # print(d)
        name = d.find('span', attrs={'class': 'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        # print(n[0]['alt'])
        author = d.find('a', attrs={'class': 'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class': 'a-icon-alt'})
        users_rated = d.find('a', attrs={'class': 'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class': 'p13n-sc-price'})

        # all1=[]

        if name is not None:
            # print(n[0]['alt'])
            book_name = n[0]['alt']


        else:
            # all1.append("unknown-product")
            book_name = 'unknown-product'

        if author is not None:
            # print(author.text)
            author_name = author.text
        elif author is None:
            author = d.find('span', attrs={'class': 'a-size-small a-color-base'})
            if author is not None:
                author_name = author.text
            else:
                author_name = 'anonymous'

        if rating is not None:
            # print(rating.text)
            rate = rating.text
            k = rate.split('out')
            rate = k[0]
        else:
            rate = -1

        if users_rated is not None:
            # print(price.text)
            users = users_rated.text
        else:
            users = -1

        if price is not None:
            # print(price.text)
            book_price = price.text
            p = book_price.split('₹')
            book_price = p[1]
            # print(book_price)
        else:
            book_price = 0

        cur.execute('''INSERT OR IGNORE INTO Books (Book_name, Author, Rating, Customers_rated, Price)
                VALUES ( ?, ?, ?, ?, ? )''', (book_name, author_name, rate, users, book_price))
        
    conn.commit()


for i in range(1, no_pages + 1):
    get_data(i)


