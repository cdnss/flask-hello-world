from flask import Flask
from selenium import webdriver
#from IPython.display import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json,os

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)
#wait = WebDriverWait(driver, 10)
#driver.implicitly_wait(5)
driver.get("https://samehadaku.guru/")
#wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))




#print(innerHTML)
#display(HTML(driver.find_element(BY_TAG_NAME('html')))

driver.quit()
app = Flask(__name__)

@app.route('/')
def home():
    return driver.page_source

@app.route('/about')
def about():
    return 'About'
