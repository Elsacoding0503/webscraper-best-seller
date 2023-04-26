# 博客來暢銷書
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd
from sqlalchemy import Integer, Text
import credential

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

url_books = 'https://www.books.com.tw/web/sys_saletopb/books/?attribute=30'
response_books = requests.get(url=url_books, headers=headers)
soup_books = bs(response_books.text, 'lxml')

title = [(i.text.strip().split('\n'))[0] for i in soup_books.find_all('div', {'class':'type02_bd-a'})]
author = [i.text.strip().split('\n')[2].split('：')[1] for i in soup_books.find_all('div', {'class':'type02_bd-a'})]
ranking = [i.text.strip().split('P')[1] for i in soup_books.find_all('div', {'class':'stitle'})]

price = []
raw_price = [i.text.strip().split('\n')[3].split('：')[1] for i in soup_books.find_all('div', {'class':'type02_bd-a'})]
for i in raw_price:
    try:
        price.append(i.split('折')[1].replace('元',''))
    except:
        price.append((i).replace('元',''))
url = [i.find('a')['href'] for i in soup_books.find_all('div', {'class':'type02_bd-a'})]

        
dict_books = {}
dict_books['title'] = title
dict_books['author'] = author
dict_books['ranking'] = ranking
dict_books['price'] = price
dict_books['url'] = url
df_books = pd.DataFrame(dict_books)

engine = credential.engine
dtypedict = {
'title': Text(),
'author': Text(),
'ranking': Integer(),    
'price': Integer(),
'url': Text(),
}

df_books.to_sql(name='博客來',con=engine.connect(), if_exists='replace',dtype=dtypedict,index=False)

with engine.connect() as conn:
    conn.execute('''ALTER TABLE 博客來 \
    ADD COLUMN id SERIAL PRIMARY KEY
    '''
    )