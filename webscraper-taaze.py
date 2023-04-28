# 讀冊暢銷
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd
from sqlalchemy import Integer, Text
import credential
import time,random

ua = UserAgent()
headers = {
    'user-agent': ua.random
}

all_taaze = []
for i in range(1,6):
    startnum=0
    endnum=23
    
    params = {
        'a': '01',
        'd': '00',
        'l': '0',
        't': '11',
        'c': '00',
        'k': '01',
        'startNum': startnum,
        'endNum': endnum,
        'sortType': '1',
    }
    startnum+=24
    endnum+=24
    
    url_taaze = 'https://www.taaze.tw/beta/actAllBooksDataAgent.jsp'
    response_taaze = requests.get(url=url_taaze, params=params, headers=headers)
    result_tazze = response_taaze.json()
    for result in result_tazze['result1']:
        all_taaze.append(result)
print(len(all_taaze))

titile = [i['titleMain'] for i in all_taaze]
author = [i['author'] for i in all_taaze]
ranking = [i for i,j in enumerate(all_taaze)]
price = [i['salePrice'] for i in all_taaze]
url = ['https://www.taaze.tw/products/' + i['prodId'] + '.html' for i in all_taaze]

isbn = []
for u in url:
    res_taaze = requests.get(url=u, headers=headers)
    soup_taaze = bs(res_taaze.text, 'lxml')
    try:
        isbn.append(soup_taaze.find_all('div', {'style':'margin:2px 0;'})[1].text.split('：')[3])
    except:
        isbn.append('')
    time.sleep(random.uniform(1,3))

dict_taaze = {}
dict_taaze['titile'] = titile
dict_taaze['author'] = author
dict_taaze['ranking'] = ranking
dict_taaze['price'] = price
dict_taaze['url'] = url
dict_taaze['isbn'] = isbn

df_taaze = pd.DataFrame(dict_taaze)

engine = credential.engine
dtypedict = {
'title': Text(),
'author': Text(),
'ranking': Integer(),    
'price': Integer(),
'url': Text(),
'isbn': Text(),
}

df_taaze.to_sql(name='讀冊',con=engine.connect(), if_exists='replace',dtype=dtypedict,index=False)

with engine.connect() as conn:
    conn.execute(
        '''ALTER TABLE 讀冊 \
    ADD COLUMN id SERIAL PRIMARY KEY
    ''')

with engine.connect() as conn:
    conn.execute(
    '''
    ALTER TABLE public.讀冊 ADD book_store varchar NULL DEFAULT '讀冊';
    '''
    )