from mit_calendar import *
from src.recommender.recommender import *
from src.scraper.constants import *
from src.scraper.eventbrite import *
import pandas as pd
from datetime import datetime
from dateutil import parser

def run1():

    df = pd.read_csv("data_pair.tsv", sep='\t')

    df = df.drop_duplicates(subset='What is your name?', keep="first")

    interests = 'Select all that interest you. This will help us personalize events for you!'
    sparse = df[interests].str.get_dummies(', ')
    z = sparse[sparse.duplicated(keep=False)]
    dups = z.groupby(list(z)).apply(lambda x: list(x.index)).tolist()

    dups.sort(key=len, reverse=True)

    #
    #
    # GROUP_1 = df_c.loc[list(a_5.index)]
    #
    # # GROUP_1.sort_values('How often would you like to receive tailored recommendations?')
    # GROUP_1_weekly = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every week"]
    # GROUP_1_couple = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every couple days"]
    # GROUP_1 = GROUP_1_weekly.append(GROUP_1_couple)
    #
    # group_1_users = []
    #
    # for index, row in GROUP_1.iterrows():
    #     user = User(row['What is your name?'], row['Select all that interest you. This will help us personalize events for you!'], row['What is your email?'])
    #     group_1_users.append(user)
    #
    # print([user.email for user in group_1_users])



def run():
    df = pd.read_csv("data_pair.tsv", sep='\t')
    df_c = df.copy()
    df = df.drop_duplicates(subset='What is your name?', keep="first")

    interests = 'Select all that interest you. This will help us personalize events for you!'
    sparse = df[interests].str.get_dummies(', ')
    z = sparse[sparse.duplicated(keep=False)]
    dups = z.groupby(list(z)).apply(lambda x: list(x.index)).tolist()

    dups.sort(key=len, reverse=True)

    # print(df_c.loc[dups[0]])

    print(sparse)


    DATES = [(8, i) for i in range(10, 18)]
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

    for e in evts_eventbrite:
        start = e['start_date'][0]
        end = e['end_date'][0]
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

    input("done... !")

    while True:
        a = input("start")
        b = input()
        c = input()
        d = input()
        e = input()
        f = input()

        a_1 = sparse[sparse[a] == int(b)]
        a_2 = a_1[a_1[c] == int(d)]
        a_5 = a_2[a_2[e] == int(f)]
        # a_4 = a_3[a_3['Theatre & Movies'] == 0]
        # a_5 = a_4[a_4['Wellness'] == 1]

        GROUP_1 = df_c.loc[list(a_5.index)]

        # GROUP_1.sort_values('How often would you like to receive tailored recommendations?')
        GROUP_1_weekly = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every week"]
        GROUP_1_couple = GROUP_1[GROUP_1['How often would you like to receive tailored recommendations?'] == "Every couple days"]
        GROUP_1 = GROUP_1_weekly.append(GROUP_1_couple)

        group_1_users = []

        for index, row in GROUP_1.iterrows():
            user = User(row['What is your name?'], row['Select all that interest you. This will help us personalize events for you!'], row['What is your email?'])
            group_1_users.append(user)

        print([user.email for user in group_1_users])

        print(len(all_events))
        user = group_1_users[0]
        sim = get_most_similar(user, all_events, 20)
        txt = user.generate_email_for_events(sim)
        print(txt)
        print("")
        print("*" * 20)
        print("")
        print("")