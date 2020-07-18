import ast

class Database:
    def __init__(self, path):
        self.location = path
        self.events = self._load_events(self.location)
    
    def _load_events(self, path):
        file = open(path, "r")
        contents = file.read()
        events_list = eval(contents)
        file.close()
        
        return [self._convert_event(event) for event in events_list]

    
    def _convert_event(self, event_dict):
        event_obj = Event(name=event_dict['name'], description = event_dict['description'], tags = event_dict['tags'], start_date = event_dict['start_date'], 
        end_date = event_dict['end_date'], url = event_dict['url'], event_id = event_dict['event_id'], image = event_dict['image'], min_ticket_price = event_dict['min_ticket_price'],
        max_ticket_price = event_dict['max_ticket_price'], has_available_tickets = event_dict['has_available_tickets'], tickets_url = event_dict['tickets_url'], 
        is_online_event = event_dict['is_online_event'])
        return event_obj


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