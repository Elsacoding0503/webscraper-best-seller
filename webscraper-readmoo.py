# 讀墨暢銷
from bs4 import BeautifulSoup as bs
import pandas as pd
from sqlalchemy import Integer, Text
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent 
from selenium.webdriver.chrome.options import Options
import credential
import requests
import time, random


ua = UserAgent()
options = Options() 
# options.add_argument('--headless') 
options.add_argument("user-agent=" + ua.chrome)
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)


url_readmoo = 'https://readmoo.com/leaderboard/book/sale/'
driver.get(url_readmoo) 
driver.maximize_window()

# title = driver.find_elements(By.CLASS_NAME, 'title')
soup_readmoo = bs(driver.page_source, 'lxml')
title = [i.text for i in soup_readmoo.find_all('h2', {'class':'title'})]
author = [i.text for i in soup_readmoo.find_all('div', 'contributor-info')]
ranking = [i+1 for i,j in enumerate(title)]
price = [i.text.split('$')[1] for i in soup_readmoo.find_all('span', 'price our-price')]
url = [i.a['href'] for i in soup_readmoo.find_all('h2', {'class':'title'})]

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

isbn = []
for u in url:
    readmoo_detail = requests.get(url=u, headers=headers)
    soup_detail = bs(readmoo_detail.text,'lxml')
    try:
        isbn.append(soup_detail.find("span", {'itemprop': 'isbn'}).text)
    except:
        isbn.append('')
    time.sleep(random.uniform(1,3))

print(len(title))
print(len(author))
print(len(ranking))
print(len(price))
print(len(url))
print(len(isbn))    

dict_readmoo = {}
dict_readmoo['title'] = title
dict_readmoo['author'] = author
dict_readmoo['ranking'] = ranking
dict_readmoo['price'] = price
dict_readmoo['url'] = url
dict_readmoo['isbn'] = isbn

df_readmoo = pd.DataFrame(dict_readmoo)
engine = credential.engine
dtypedict = {
'title': Text(),
'author': Text(),
'ranking': Integer(),    
'price': Integer(),
'url': Text(),
'isbn': Text(),
}

df_readmoo.to_sql(name='讀墨',con=engine.connect(), if_exists='replace',dtype=dtypedict,index=False)

with engine.connect() as conn:
    conn.execute(
        '''ALTER TABLE 讀墨 \
    ADD COLUMN id SERIAL PRIMARY KEY
    ''')

driver.close()