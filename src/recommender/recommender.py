from config import *
import time, math
import random
from datetime import date, timedelta
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from src.recommender.database import Database
from src.recommender.config import *

class User:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.keywords = tags #self.get_keywords(tags)

    def get_keywords(self, tags):
        keywords = []
        for tag in tags:
            tag.replace(' ', '')
            words = tag.split('&/')
            keywords.extend(words.lower())
        return list(set(keywords))

    def _subset(self, keywords):
        return random.sample(keywords, min(1,len(keywords//3)))

    def generate_ideal_event(self, random_tags = False, num=5):
        events = []

        for i in range(num):
            name = ""
            description = ""
            tags = self._subset(self.keywords) if random_tags else self.keywords
            start_date = date.today() + timedelta(days=3+i)
            end_date = date.today() + timedelta(days=3+i)
            start_time = 10 + 2*i #in EDT
            end_time = 11 + 2*i
            events.append(Event(name, description, tags, start_date, end_date, start_time, end_time, ""))

        return events




class RecommenderModel:
    def __init__(self, path=None):
        location = DATABASE_PATH if path is None else path
        self.events = self._load_events(location)
        self.best_matches = []

        self.tag_weight = 3
        self.description_weight = 1
        self.name_weight = 4


    def _load_events(self, path):
<<<<<<< HEAD
        location = DATABASE_PATH if path is None else path
        events = [] # TODO: Implement me!
        return events

=======
        database = Database(path)
        return database.events

>>>>>>> 84251d4fb6e01ca2bc4506cacebd4b620a904238

    def _get_relevant_events(self, start_date, end_date):
        rel_events = []
        for event in self.events:
            #   TODO: change the indexing :(
            if event.start_date[0] > start_date and event.start_date[0] <= end_date:
                rel_events += event
        return rel_events


    def _get_match_score(self, event, user):
        keywords = user.keywords

        tag_score = 0
        for tag in event.tags:
            for keyword in keywords:
                keyword_lower = keyword.lower()
                tag_lower = tag.lower()
                tag_score += self.tag_weight if keyword_lower in tag_lower else 0

        description_score = 0
        for keyword in keywords:
<<<<<<< HEAD
            description_score += self.description_weight if keyword in event.description else 0

=======
            keyword_lower = keyword.lower()
            description_lower = event.description.lower()
            description_score += self.description_weight if keyword_lower in description_lower else 0

>>>>>>> 84251d4fb6e01ca2bc4506cacebd4b620a904238
        name_score = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            name_lower = event.name.lower()
            name_score += self.name_weight if keyword_lower in name_lower else 0

        cumulative_score = tag_score + description_score + name_score
        return cumulative_score


    def fit(self, user, start_date, end_date):
        events = self._get_relevant_events(start_date, end_date)
        event_scores = []
        for event in events:
            score = self._get_match_score(event, user)
            event_scores.append((score, event))

        event_scores.sort(reverse=True)
        self.best_matches = [e[1] for e in event_scores]


    def get_matches(self, number=None):
        last_index = len(self.best_matches) if number is None else number
        return self.best_matches[:last_index]
<<<<<<< HEAD


class Event:
    def __init__(self, name, description, tags, start_date, end_date, start_time, end_time, url, event_id=None, image=None,
                min_ticket_price=None, max_ticket_price=None, has_available_tickets=None, tickets_url=None, is_online_event=None):
        self.name = name
        self.description = description
        self.tags = tags
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.url = url
        self.event_id = event_id
        self.image = image
        self.min_ticket_price = min_ticket_price
        self.max_ticket_price = max_ticket_price
        self.has_available_tickets = has_available_tickets
        self.tickets_url = tickets_url
        self.is_online_event = is_online_event

def get_most_similar(user, all_events, num_events):
    if num_events > len(all_events):
        raise ValueError("You asked for more events than exist...")

    ideal_events = user.generate_ideal_event(num=3)
    similarity_scores = np.zeros((len(ideal_events), len(all_events)))
    for i in range(len(ideal_events)):
        for j in range(len(all_events)):
            similarity_scores[i,j] = similarity(ideal_events[i], all_events[j])

    top_indices = np.argmax(similarity_scores, axis=1)
    # print(similarity_scores)
    # print(np.sort(similarity_scores, axis=1))
    probs = np.sum(similarity_scores, axis=0)
    probs /= np.sum(probs)
    idxs = np.random.choice(list(range(len(all_events))), p = probs, replace=False, size=num_events)
    return [all_events[j] for j in idxs]

def similarity(event1, event2):
    # name = ""
    # description = ""
    # tags = self._subset(self.keywords) if random_tags else self.keywords
    # start_date = date.today() + timedelta(days=3 + i)
    # end_date = date.today() + timedelta(days=3 + i)
    # start_time = 10 + 2 * i  # in EDT
    # end_time = 11 + 2 * i

    total = 0
    total += _tag_similarity(event1.tags, event2.tags)
    total += abs(6-(event1.start_date.weekday() - event2.start_date.weekday()))
    total += abs(6-(event1.end_date.weekday() - event2.end_date.weekday()))
    total += abs(24-(event1.start_time - event2.start_time))

    return total

    # tags = [event1.tags, event2.tags]
    # vect = TfidfVectorizer(min_df=1, stop_words="english")
    # tfidf = vect.fit_transform(tags)
    # pairwise_similarity = tfidf * tfidf.T

def _tag_similarity(tags1, tags2):
    freq = 0
    for t1 in tags1:
        for t2 in tags2:
            if t1==t2:
                freq+=1
    return freq
if __name__ == "__main__":
    user1 = User("Baptiste Bouvier", ["entrepreneurship", "virtual", "politics", "spanish"])

    events = []
    events.append(Event("name", "description", ['entepreneurship', 'marketing', 'business'], date.today(), date.today(), 14, 15, "url"))
    events.append(Event("name", "description", ['spanish', 'MIT', 'business'], date.today()+timedelta(days=1), date.today()+timedelta(days=1), 17, 19, "url"))
    events.append(Event("name", "description", ['japanese', 'in person', 'recruiting'], date.today()+timedelta(days=2), date.today()+timedelta(days=2), 9, 9.5, "url"))
    events.append(Event("name", "description", ['computer', 'MIT', 'business'], date.today()+timedelta(days=3), date.today()+timedelta(days=13), 11, 12, "url"))
    events.append(Event("name", "description", ['literature', 'shakespeare', 'film'], date.today()+timedelta(days=4), date.today()+timedelta(days=4), 16, 17.5, "url"))
    a = get_most_similar(user1, events, 2)

    print(a)
=======
>>>>>>> 84251d4fb6e01ca2bc4506cacebd4b620a904238
