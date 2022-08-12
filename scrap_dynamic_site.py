import time

path = 'C:\\Users\\sin-yee.teoh\\Downloads\\chromedriver_win32\\chromedriver.exe'

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

options = Options()
options.add_argument("start-maximized")
options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

driver.get("https://quotes.toscrape.com/js/")

soup = BeautifulSoup(driver.page_source, features='html.parser')

h1 = soup.find("h1")
#print(h1)

videos = driver.find_element(By.CLASS_NAME, "author")
print(videos.text)
