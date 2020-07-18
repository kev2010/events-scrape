import datetime

from src.recommender.recommender import User, RecommenderModel

user = User('Kevin', ['Business', 'Environment', 'Future'])
model = RecommenderModel()
start = datetime.datetime.now()
end = datetime.datetime(year=2020, month=6, day=15)
model.fit(user, start, end)
print(model.get_matches())
