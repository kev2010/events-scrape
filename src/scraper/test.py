import requests
import json
import gql
import pprint
from gql import client
import time
from constants import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

from bs4 import BeautifulSoup

#   chromedriver options setup
chrome_options = Options()
chrome_options.add_argument("--headless")

def scrape_events():
    for url in URLS_TO_VISIT:
        driver = webdriver.Chrome(CHROMEDRIVER_LOC, options=chrome_options)
        print(url)
        driver.get(url)

        def process_browser_log_entry(entry):
            response = json.loads(entry['message'])['message']
            return response

        browser_log = driver.get_log('performance') 
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.response' in event['method']]

        print(browser_log)
        print("lol")
        print(events)

        # soup = BeautifulSoup(driver.page_source, 'lxml')

        # event_name = soup.find('title', {'id': 'pageTitle'}).text
        # blurb = soup.find('div', {'id': 'title_subtitle'})
        # event_date = blurb.find('span').get('aria-label')
        # host = soup.find('div', {'data-testid': 'event_permalink_feature_line'}).get('content')
        # location = soup.find('span', {'class': '_5xhk'}).text
        # print(event_name)
        # print(event_date)
        # print(host)
        # print(location)


def get_request(url, params):
    """
    spec
    """
    r = requests.get(url=url, params=params)
    data = r.json()
    return data

if __name__ == "__main__":
    scrape_events()
