from src.recommender.database import Database
from src.recommender.config import *

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
            keywords.extend(words)
        return keywords
        

class RecommenderModel:
    def __init__(self, path=None):
        location = DATABASE_PATH if path is None else path
        self.events = self._load_events(location)
        self.best_matches = []

        self.tag_weight = 3
        self.description_weight = 1
        self.name_weight = 4
        
    
    def _load_events(self, path):
        database = Database(path)
        return database.events
    

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
            keyword_lower = keyword.lower()
            description_lower = event.description.lower()
            description_score += self.description_weight if keyword_lower in description_lower else 0
        
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
