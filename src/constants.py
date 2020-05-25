#   Chromedriver setup
CHROMEDRIVER_LOC = "./chromedriver"

#   URLs to scrape
#   Note that we look at online events from pages 1 to 50 because EventBrite only displays 1000 events, rest are hidden
#   TODO: change the URL if you're trying to scrape something other than online events
URLS_TO_VISIT = ["https://www.eventbrite.com/d/online/all-events/?page=" + str(i) for i in range(1, 51)]
#   EventBrite categories
BUSINESS_EVENTS = ["https://www.eventbrite.com/d/online/business--events/?page=" + str(i) for i in range(1, 51)]
FOOD_DRINK_EVENTS = ["https://www.eventbrite.com/d/online/food-and-drink--events/?page=" + str(i) for i in range(1, 51)]
HEALTH_EVENTS = ["https://www.eventbrite.com/d/online/health--events/?page=" + str(i) for i in range(1, 51)]
MUSIC_EVENTS = ["https://www.eventbrite.com/d/online/music--events/?page=" + str(i) for i in range(1, 51)]
AUTO_BOAT_AIR_EVENTS = ["https://www.eventbrite.com/d/online/auto-boat-and-air--events/?page=" + str(i) for i in range(1, 51)]
CHARITY_CAUSES_EVENTS = ["https://www.eventbrite.com/d/online/charity-and-causes--events/?page=" + str(i) for i in range(1, 51)]
COMMUNITY_EVENTS = ["https://www.eventbrite.com/d/online/community--events/?page=" + str(i) for i in range(1, 51)]
FAMILY_EVENTS = ["https://www.eventbrite.com/d/online/family-and-education--events/?page=" + str(i) for i in range(1, 51)]
FASHION_EVENTS = ["https://www.eventbrite.com/d/online/fashion--events/?page=1"]
FILM_MEDIA_EVENTS = ["https://www.eventbrite.com/d/online/film-and-media--events/?page=" + str(i) for i in range(1, 51)]
HOBBIES_EVENTS = ["https://www.eventbrite.com/d/online/hobbies--events/?page=" + str(i) for i in range(1, 51)]
HOME_LIFESTYLE_EVENTS = ["https://www.eventbrite.com/d/online/home-and-lifestyle--events/?page=" + str(i) for i in range(1, 51)]
PERFORMING_VISUAL_ARTS_EVENTS = ["https://www.eventbrite.com/d/online/arts--events/?page=" + str(i) for i in range(1, 51)]
GOVERNMENT_EVENTS = ["https://www.eventbrite.com/d/online/government--events/?page=" + str(i) for i in range(1, 51)]
SPIRITUALITY_EVENTS = ["https://www.eventbrite.com/d/online/spirituality--events/?page=" + str(i) for i in range(1, 51)]
SCHOOL_ACTIVITIES_EVENTS = ["https://www.eventbrite.com/d/online/school-activities--events/?page=" + str(i) for i in range(1, 51)]
SCIENCE_TECH_EVENTS = ["https://www.eventbrite.com/d/online/science-and-tech--events/?page=" + str(i) for i in range(1, 51)]
HOLIDAY_EVENTS = ["https://www.eventbrite.com/d/online/holiday--events/?page=" + str(i) for i in range(1, 51)]
SPORTS_FITNESS_EVENTS = ["https://www.eventbrite.com/d/online/sports-and-fitness--events/?page=" + str(i) for i in range(1, 51)]
TRAVEL_OUTDOOR_EVENTS = ["https://www.eventbrite.com/d/online/travel-and-outdoor--events/?page=" + str(i) for i in range(1, 51)]
OTHER = ["https://www.eventbrite.com/d/online/other--events/?page=" + str(i) for i in range(1, 51)]

#   EventBrite API - used to get event information
API_URL = "https://www.eventbrite.com/api/v3/destination/events/?"

