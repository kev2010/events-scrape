import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from constants import CHROMEDRIVER_LOC


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(CHROMEDRIVER_LOC, options=chrome_options)

def get_categories(categories_url):
    resp = requests.get(categories_url)
    soup = BeautifulSoup(resp.content, features='xml')
    events = soup.findAll('item')

    all_events = {}
    for event in events:
        event_item = {}
        url = event.link.text
        categories = [category.text for category in event.find_all('category')]
        all_events[url] = categories
    return all_events


def save_events(path, events):
    with open(path, 'w') as file:
        file.write(str(events))


def scrape_events_mit(urls, categories_url, path=None):
    categories = get_categories(categories_url)
    all_events = []
    for url in urls:
        print(f'Processing {url}')
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        events_html = soup.find_all('script', type='application/ld+json')
        for event_json in events_html:
            event = json.loads(event_json.get_text())[0]
            title = event['name']
            description = event['description']
            start_date  = event['startDate']
            end_date = event['endDate']
            url = event['url']
            ticket_price = event['offers']['price'] if 'offers' in event.keys() else 0

            if url[:5] != 'https':
                url = url[:4] + 's' + url[4:]
            tags = categories[url]
            all_events.append({
                'name': title,
                'description': description,
                'tags': tags,
                'start_date': start_date,
                'end_date': end_date,
                'url': url,
                'ticket_price': ticket_price
            })
    if path is None:
        return all_events
    save_events(path, all_events)

if __name__ == "__main__":
    DATES = [(7, i) for i in range(21, 28)]
    urls = [f'https://calendar.mit.edu/calendar/day/2020/{m}/{d}' for m, d in DATES]
    categories_url = 'https://calendar.mit.edu/search/events.xml'

    print(scrape_events(urls, categories_url))