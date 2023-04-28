# 金石堂暢銷
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd
from sqlalchemy import Integer, Text
import credential
import time, random

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

url_kingstone = 'https://www.kingstone.com.tw/bestseller/best/book?ranktype=y'
response_kingstone = requests.get(url=url_kingstone, headers=headers)
soup_kingstone = bs(response_kingstone.text, 'lxml')

cookies = response_kingstone.cookies.get_dict()
jar = requests.utils.cookiejar_from_dict(cookies)

title = [i.text.strip() for i in soup_kingstone.find_all('div', 'modProName')]
author = [i.text for i in soup_kingstone.find_all('a', 'mProBlue')]
ranking = [i.text.strip().split('P')[1] for i in soup_kingstone.find_all('div', 'modProRank')]
price = [i.text.split('特價')[1].replace('元','') for i in soup_kingstone.find_all('div', 'priceset')]
url = [i.a['href'] for i in soup_kingstone.find_all('div', 'modProName')]

isbn = []
rs = requests.session()
for u in url:
    kingstone_response = rs.get(url=u, headers=headers, cookies=jar)
    kingstone_soup = bs(kingstone_response.text, 'lxml')
    isbn.append(kingstone_soup.find_all('li', 'table_td')[3].text)
    time.sleep(random.uniform(1,3))

print(len(title))
print(len(author))
print(len(ranking))
print(len(price))
print(len(url))
print(len(isbn))


dict_kingstone = {}
dict_kingstone['title'] = title
dict_kingstone['author'] = author
dict_kingstone['ranking'] = ranking
dict_kingstone['price'] = price
dict_kingstone['url'] = url
dict_kingstone['isbn'] = isbn
df_kingstone = pd.DataFrame(dict_kingstone)

engine = credential.engine
dtypedict = {
'title': Text(),
'author': Text(),
'ranking': Integer(),    
'price': Integer(),
'url': Text(),
'isbn': Text(),
}

df_kingstone.to_sql(name='金石堂',con=engine.connect(), if_exists='replace',dtype=dtypedict,index=False)

with engine.connect() as conn:
    conn.execute(
        '''ALTER TABLE 金石堂 \
    ADD COLUMN id SERIAL PRIMARY KEY
    ''')

with engine.connect() as conn:
    conn.execute(
    '''
    ALTER TABLE public.金石堂 ADD book_store varchar NULL DEFAULT '金石堂';
    '''
    )