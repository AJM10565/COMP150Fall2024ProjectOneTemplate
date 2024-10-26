import json
import sys
import random
from typing import List, Optional
from enum import Enum
from src.character import Character



class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))



class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True

    def start(self):
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False
        print("Game Over.")

    def check_game_over(self):
        return len(self.party) == 0


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()
    characters = [Character(f"Character_{i}") for i in range(3)]

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()

# Unit Test for Statistic.modify method
strength = Statistic("Strength", value=50)
strength.modify(10)
assert strength.value == 60, "Strength should be 60 after increasing by 10"
strength.modify(-70)
assert strength.value == 0, "Strength should not go below 0"
strength.modify(200)
assert strength.value == 100, "Strength should not exceed 100"

# Test Statistic __str__ method
assert str(strength) == "Strength: 100", f"Expected 'Strength: 100', got {str(strength)}"

# Unit Test for Character creation and get_stats method
character = Character("Alice")
assert character.name == "Alice", "Character name should be 'Alice'"
stats = character.get_stats()
assert len(stats) == 2, "Character should have 2 stats"
assert stats[0].name == "Strength", "First stat should be 'Strength'"
assert stats[1].name == "Intelligence", "Second stat should be 'Intelligence'"

# Test Event execution for pass, partial pass, and fail
event_data = {
    'primary_attribute': 'Strength',
    'secondary_attribute': 'Intelligence',
    'prompt_text': 'You encounter a challenge.',
    'pass': {'message': 'You passed!'},
    'fail': {'message': 'You failed!'},
    'partial_pass': {'message': 'Partial success.'}
}
event = Event(event_data)

# Mock parser
parser = MagicMock()

# Unit Test for passing scenarios
parser.select_party_member.return_value = character
parser.select_stat.return_value = character.strength  # choosing Strength (primary attribute)
event.execute([character], parser)
assert event.status == EventStatus.PASS, "Event status should be PASS"
print("PASS: You passed!")

# Test partial pass scenario
parser.select_stat.return_value = character.intelligence  # choosing Intelligence (secondary attribute)
event.execute([character], parser)
assert event.status == EventStatus.PARTIAL_PASS, "Event status should be PARTIAL_PASS"
print("PARTIAL_PASS: Partial success.")

# Test fail scenario
character.strength.name = "Luck"  # non-matching attribute
parser.select_stat.return_value = character.strength
event.execute([character], parser)
assert event.status == EventStatus.FAIL, "Event status should be FAIL"
print("FAIL: You failed!")

# Test Game start and end flow
characters = [Character("Char1"), Character("Char2")]
location = Location([event])

game = Game(parser, characters, [location])

# Mock event execution to stop game loop
event.execute = lambda x, y: setattr(game, 'continue_playing', False)
game.start()
print("Game Over.")