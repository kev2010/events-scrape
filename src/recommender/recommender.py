from config import *

class User:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.keywords = self.get_keywords(tags)

    def get_keywords(self, tags):
        keywords = []
        for tag in tags:
            tag.replace(' ', '')
            words = tag.split('&/')
            keywords.extend(words.lower())
        return list(set(keywords))


class RecommenderModel:
    def __init__(self, path=None):
        self.events = self._load_events(path)
        self.best_matches = []

        self.tag_weight = 3
        self.description_weight = 1
        self.name_weight = 4


    def _load_events(self, path):
        location = DATABASE_PATH if path is None else path
        events = [] # TODO: Implement me!
        return events


    def _get_relevant_events(self, start_date, end_date):
        rel_events = []
        for event in self.events:
            if event.start_date > start_date and event.start_date <= end_date:
                rel_events += event
        return rel_events


    def _get_match_score(self, event, user):
        keywords = user.keywords

        tag_score = 0
        for tag in event.tags:
            for keyword in keywords:
                tag_score += self.tag_weight if keyword in tag else 0

        description_score = 0
        for keyword in keywords:
            description_score += self.description_weight if keyword in event.description else 0

        name_score = 0
        for keyword in keywords:
            name_score += self.name_weight if keyword in event.name else 0

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


class Event:
    def __init__(self, name, description, tags, start_date, end_date, url, event_id=None, image=None,
                min_ticket_price=None, max_ticket_price=None, has_available_tickets=None, tickets_url=None, is_online_event=None):
        self.name = name
        self.description = description
        self.tags = tags
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.event_id = event_id
        self.image = image
        self.min_ticket_price = min_ticket_price
        self.max_ticket_price = max_ticket_price
        self.has_available_tickets = has_available_tickets
        self.tickets_url = tickets_url
        self.is_online_event = is_online_event
