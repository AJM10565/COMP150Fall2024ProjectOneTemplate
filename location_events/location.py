import json
import random
from typing import List
from location_events.event import Event

class Location:
    def __init__(self, location_info, events):
        self.location_info = location_info
        self.events = events


    def get_event(self) -> Event:
        return random.choice(self.events)

def load_event_from_json(filepath: str) -> Event:
    with open(filepath, "r") as f:
        data = json.load(f)
        return Event(data)