import json
import random
from typing import List
from event import Event, EventStatus

class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)

def load_event_from_json(filepath: str) -> Event:
    with open(filepath, "r") as f:
        data = json.load(f)
        return Event(data)