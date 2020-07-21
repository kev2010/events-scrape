import json
import datetime
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from constants import *

#   Options setup
chrome_options = Options()
chrome_options.add_argument("--headless")
#   Capabilities to get network traffic
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = { 'performance':'ALL' }
#   Set up driver
driver = webdriver.Chrome(CHROMEDRIVER_LOC, desired_capabilities=caps, options=chrome_options)

def scrape_events(path, urls):
    """
    Scrapes the given EventBrite urls.

    Args:
        urls (list of str): the urls to scrape
    Returns:
        list of lists where each list entry contains information about an event
    """
    seen_ids = set()
    result = []
    for url in urls:
        #   Get all of the Network requests being sent out
        print(f'Processing {url}')
        driver.get(url)
        browser_log = driver.get_log('performance') 
        events = [process_browser_log_entry(entry) for entry in browser_log]
        results = []
        #   Find the Network request that sends a GET request to EventBrite API
        for event in events:
            if event['method'] == 'Network.responseReceived':
                # print(event)
                if 'event_ids' in event['params']['response']['url']:
                    results.append(event)
        #   Get the GET request URL
        get_url = ""
        #   TODO: Sometimes returning 0 or more than 1... I'm not sure why :(
        if len(results) >= 1:
            get_url = results[0]['params']['response']['url']
            #   Get the GET request response JSON
            json_response = get_request(get_url)
            event_list = json_response['events']
            #   Find unique events in the response JSON 
            unique_event_list = []
            for event in event_list:
                if event['id'] not in seen_ids:
                    seen_ids.add(event['id'])
                    unique_event_list.append(event)
            parsed_events = parse_event_page(unique_event_list)
            result.extend(parsed_events)
        else:
            print(results)
            print('yikes something went wrong')
    
    save_events(path, result)
    driver.close()


def process_browser_log_entry(entry):
    """
    spec
    """
    response = json.loads(entry['message'])['message']
    return response


def get_request(url):
    """
    spec
    """
    r = requests.get(url)
    data = r.json()
    return data


def parse_event_page(event_page):
    """
    beautiful spec
    """
    result = []
    for event_json in event_page:
        event_dict = {
            'name': event_json['name'],
            'description': event_json['summary'],
            'tags': [tag['display_name'] for tag in event_json['tags']],
            'start_date': (datetime.datetime(year=int(event_json['start_date'][:4]), month=int(event_json['start_date'][5:7]), day=int(event_json['start_date'][8:]),
                                    hour=int(event_json['start_time'][:2]), minute=int(event_json['start_time'][3:])), event_json['timezone']),
            'end_date': (datetime.datetime(year=int(event_json['end_date'][:4]), month=int(event_json['end_date'][5:7]), day=int(event_json['end_date'][8:]),
                                    hour=int(event_json['end_time'][:2]), minute=int(event_json['end_time'][3:])), event_json['timezone']),
            'url': event_json['url'],
            'event_id': event_json['id'],
            'image': event_json['image']['url'],
            'min_ticket_price': event_json['ticket_availability']['minimum_ticket_price']['display'],
            'max_ticket_price': event_json['ticket_availability']['maximum_ticket_price']['display'],
            'has_available_tickets': not event_json['ticket_availability']['is_sold_out'],
            'tickets_url': event_json['tickets_url'],
            'is_online_event': event_json['is_online_event'],
        }
        result.append(event_dict)
    return result


def save_events(path, events):
    with open(path, 'w') as file:
        file.write(str(events))


if __name__ == "__main__":
    urls = ['https://www.eventbrite.com/d/online/business--events/?page=1']
    scrape_events(DATABASE_LOC, urls)