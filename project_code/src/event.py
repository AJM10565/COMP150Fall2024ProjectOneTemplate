import random
from typing import List
from enum import Enum
from character import Character
from random import choice


class EventStatus:
    UNKNOWN = "unknown"
    PASS = "pass"
    PARTIAL_PASS = "partial_pass"
    FAIL = "fail"

class GameEvent:
    def __init__(self, event_data):
        self.prompt_text = event_data['prompt_text']
        self.event_type = event_data['event_type']
        
        # Initialize based on event type
        if self.event_type == "battle":
            self.outcomes = event_data['outcomes']
        elif self.event_type in ["obstacle", "mysterious"]:
            self.options = event_data['options']
        self.status = EventStatus.UNKNOWN

    def execute(self, party, parser):
        print(self.prompt_text)
        if self.event_type == "battle":
            self.handle_battle_event(party)
        elif self.event_type in ["obstacle", "mysterious"]:
            self.handle_obstacle_or_mysterious_event(party, parser)

    def handle_battle_event(self, party):
        # Randomly determine battle outcome
        outcome = choice(list(self.outcomes.keys()))
        result = self.outcomes[outcome]
        health_change = result['health_change']

        for character in party:
            character.take_damage(-health_change)  # Adjust character health
        print(result['message'])
        self.status = EventStatus.PASS if outcome == 'win' else EventStatus.FAIL

    def handle_obstacle_or_mysterious_event(self, party, parser):
        print("Choose an option:")
        for idx, option in enumerate(self.options.keys(), start=1):
            print(f"{idx}. {option}")

        # Parse user input via parser
        choice_index = int(parser.parse("Enter your choice: ")) - 1
        option_key = list(self.options.keys())[choice_index]
        option = self.options[option_key]

        # Randomly determine the outcome of the selected option
        outcome = choice(list(option.keys()))
        result = option[outcome]
        health_change = result['health_change']

        # Display outcome and adjust character health as needed
        print(result['message'])
        for character in party:
            character.take_damage(-health_change)
