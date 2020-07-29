from mit_calendar import *
from src.recommender.recommender import *
from src.scraper.constants import *
from src.scraper.eventbrite import *
import pandas as pd
from datetime import datetime
from dateutil import parser

df = pd.read_csv("data_pair.tsv", sep='\t')
df_c = df.copy()
df = df.drop_duplicates(subset='What is your name?', keep="first")

interests = 'Select all that interest you. This will help us personalize events for you!'
sparse = df[interests].str.get_dummies(', ')
z = sparse[sparse.duplicated(keep=False)]
dups = z.groupby(list(z)).apply(lambda x: list(x.index)).tolist()

dups.sort(key=len, reverse=True)

# print(df_c.loc[dups[0]])

a_1 = sparse[sparse['Business & Career'] == 1]
a_2 = a_1[a_1['Technology'] == 1]
a_3 = a_2[a_2['Music'] == 1]
a_4 = a_3[a_3['Theatre & Movies'] == 1]
a_5 = a_4[a_4['Health & Fitness'] == 1]

GROUP_1 = df_c.loc[list(a_5.index)]

# GROUP_1.sort_values('How often would you like to receive tailored recommendations?')
GROUP_1_weekly = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every week"]
GROUP_1_couple = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every couple days"]
GROUP_1 = GROUP_1_weekly.append(GROUP_1_couple)

group_1_users = []

for index, row in GROUP_1.iterrows():
    user = User(row['What is your name?'], row['Select all that interest you. This will help us personalize events for you!'], row['What is your email?'])
    group_1_users.append(user)

print(len(group_1_users))

DATES = [(7, i) for i in range(25, 27)]
urls = [f'https://calendar.mit.edu/calendar/day/2020/{m}/{d}' for m, d in DATES]
categories_url = 'https://calendar.mit.edu/search/events.xml'

evts = scrape_events_mit(urls, categories_url)
# print(URLS_TO_VISIT)
evts_eventbrite = scrape_events("", URLS_TO_VISIT)

all_events = []
for e in evts:
    start = parser.parse(e['start_date'])
    end = parser.parse(e['end_date'])
    all_events.append(Event(e['name'],e['description'], e['tags'], start, end, start.hour, end.hour, e['url']))

#
# print("Checking descriptions...")
# for event in all_events:
#     print(event.description)
#     x = input()
#     if x != "":
#         e.description = x
#
# for u in group_1_users:
#     print(u.email)

print(len(all_events))
user = group_1_users[0]
sim = get_most_similar(user, all_events, 10)
txt = user.generate_email_for_events(sim)
print(txt)
print("")
print("*" * 20)
print("")
print("")