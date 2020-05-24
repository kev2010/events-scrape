#   Chromedriver setup
#   TODO: just put the path to the location of your chromedriver
CHROMEDRIVER_LOC = "./chromedriver"

#   URLs to scrape
#   Note that we look at online events from pages 1 to 50 because EventBrite only displays 1000 events, rest are hidden
#   TODO: change the URL if you're trying to scrape something other than online events
# URLS_TO_VISIT = ["https://www.eventbrite.com/d/online/all-events/?page=" + str(i) for i in range(1, 51)]
URLS_TO_VISIT = ["https://www.eventbrite.com/d/online/all-events/?page=50"]

#   EventBrite API - used to get event information
API_URL = "https://www.eventbrite.com/api/v3/destination/events/?"
EXPAND = "series,event_sales_status,primary_venue,image,saves,my_collections,ticket_availability"
PAGE_SIZE = 20

