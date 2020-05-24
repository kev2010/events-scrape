import requests
import json
import gql
import pprint
from gql import client
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count


from bs4 import BeautifulSoup


# url = "https://www.facebook.com/events/44843505" \
#       "2621047/?active_tab=discussion"

url = "https://www.facebook.com/events/269422687576001/"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("/Users/kj/Documents/projects/webscrape/test_scrape/chromedriver", options=chrome_options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

event_name = soup.find('title', {'id': 'pageTitle'}).text
blurb = soup.find('div', {'id': 'title_subtitle'})
event_date = blurb.find('span').get('aria-label')
host = soup.find('div', {'data-testid': 'event_permalink_feature_line'}).get('content')
location = soup.find('span', {'class': '_5xhk'}).text
print(event_name)
print(event_date)
print(host)
print(location)
