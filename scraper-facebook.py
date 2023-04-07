from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time,random
from fake_useragent import UserAgent 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import credential

ua = UserAgent()
options = Options() 
# options.add_argument('--headless') 
options.add_argument("user-agent=" + ua.chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url_facebook ='https://www.facebook.com/'
driver.get(url_facebook) 

email = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'pass')

email.send_keys(credential.email)
password.send_keys(credential.password)
password.submit()

time.sleep(30)



