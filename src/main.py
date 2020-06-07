import json
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
driver = webdriver.Chrome(CHROMEDRIVER_LOC, desired_capabilities=caps, chrome_options=chrome_options)


def scrape_events(urls):
    """
    some spec
    """
    result = []
    for url in urls:
        print(url)
        driver.get(url)
        browser_log = driver.get_log('performance') 
        events = [process_browser_log_entry(entry) for entry in browser_log]
        results = []

        for event in events:
            if event['method'] == 'Network.responseReceived':
                # print(event)
                if 'event_ids' in event['params']['response']['url']:
                    results.append(event)
                    # print(event)

        get_url = ""
        if len(results) == 1:
            get_url = results[0]['params']['response']['url']
        else:
            print(results)
            raise ValueError
        print(get_url)
        json_response = get_request(get_url)
        event_list = json_response['events']
        parsed_events = parse_event_page(event_list)
        result.extend(parsed_events)
    
    driver.close()
    return result


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
        event_name = event_json['name']
        event_summary = event_json['summary']
        event_tags = [tag['display_name'] for tag in event_json['tags']]
        event_url = event_json['url']
        result.append((event_name, event_summary, event_tags, event_url))
    return result


if __name__ == "__main__":
    event_list = scrape_events(URLS_TO_VISIT)
    print(event_list)
    print(len(event_list))