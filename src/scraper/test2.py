from datetime import datetime
a = "2020-07-21T10:00:00-04:00"
tim = datetime.strptime(a, '%y-%m-%dT%H:%M:%S%z')
print(tim)