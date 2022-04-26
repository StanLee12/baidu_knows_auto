#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time, json

chrome_options = Options() 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
driver.get('https://baidu.com')

login_btn = driver.find_element(By.XPATH, '//*[@id="s-top-loginbtn"]')
print(login_btn.text)

login_btn.click()

time.sleep(7)

account_file = open('account.json')

account = json.loads(account_file.read())

account_file.close()

username_input = driver.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_11__userName"]')
username_input.send_keys(account['username'])

password_input = driver.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_11__password"]')
password_input.send_keys(account['password'])

submit_btn = driver.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_11__submit"]')
submit_btn.click()



