import json
import sys
import random
from typing import List
from enum import Enum
from character import Character
from witch import Witch
from werewolf import Werewolf
from vampire import Vampire
from event import GameEvent


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Location:
    def __init__(self, events: List[GameEvent]):
        self.events = events

    def get_event(self) -> GameEvent:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.current_quest = 0
        self.continue_playing = True

    def start(self):
        while self.continue_playing and self.current_quest < 7:
            print(f"\nQuest {self.current_quest + 1}:")
            self.perform_quest()
            
            # Trigger random event after each quest, except the final quest
            if self.current_quest < 6:
                self.trigger_random_event()

            if self.check_game_over():
                print("Game Over! You have lost all characters.")
                break
            self.current_quest += 1

        if self.current_quest == 7:
            self.final_choice()

    def perform_quest(self):
        location = random.choice(self.locations)
        event = location.get_event()
        event.execute(self.party, self.parser)

    def trigger_random_event(self):
        """Trigger a random event with specified outcomes after a quest."""
        event_type = random.choice(["fight", "obstacle", "mystery"])
        
        if event_type == "fight":
            # Quick fight event
            result = random.choice(["win", "lose", "lose_health"])
            if result == "win":
                print("You won the quick fight and continue your journey.")
            elif result == "lose":
                print("You lost the quick fight and suffer a setback.")
                self.continue_playing = False  # Ends game if losing is game-ending
            else:  # lose_health
                for character in self.party:
                    character.take_damage(10)  # Example health loss
                print("You took damage in the quick fight.")

        elif event_type == "obstacle":
            # Obstacle event with 2 options
            option = self.parser.parse("Choose an option (1 or 2): ")
            if option == "1":
                print("You try to bypass the obstacle.")
                result = random.choice(["success", "hurt"])
                if result == "success":
                    print("You made it past the obstacle!")
                else:
                    for character in self.party:
                        character.take_damage(5)  # Example health loss
                    print("You got hurt trying to bypass the obstacle.")
            else:
                print("You chose a different route.")
                result = random.choice(["success", "hurt"])
                if result == "success":
                    print("You avoided the danger.")
                else:
                    for character in self.party:
                        character.take_damage(5)
                    print("You were hurt by hidden dangers.")

        elif event_type == "mystery":
            # Mystery event with 2 options
            option = self.parser.parse("You encounter a mystery. Choose an option (1 or 2): ")
            if option == "1":
                result = random.choice(["health_potion", "nothing"])
                if result == "health_potion":
                    for character in self.party:
                        character.heal(20)  # Example healing amount
                    print("You found a health potion!")
                else:
                    print("You found nothing of value.")
            else:
                result = random.choice(["health_potion", "nothing"])
                if result == "health_potion":
                    for character in self.party:
                        character.heal(20)
                    print("You found a health potion!")
                else:
                    print("There was nothing there.")

    def check_game_over(self):
        return all(character.health <= 0 for character in self.party)

    def final_choice(self):
        print("Final challenge! Make a defining choice.")
        # Implement your final choice logic here (win/lose conditions)


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name} (HP: {member.health})")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]


def load_events_from_json(file_path: str) -> List[GameEvent]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [GameEvent(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()
    
    # Character selection
    print("Choose your character:")
    print("1. Witch")
    print("2. Werewolf")
    print("3. Vampire")
    choice = int(input("Enter the number of the chosen character: "))
    
    if choice == 1:
        character = Witch("Witch")
    elif choice == 2:
        character = Werewolf("Werewolf")
    elif choice == 3:
        character = Vampire("Vampire")
    else:
        print("Invalid choice! Defaulting to Witch.")
        character = Witch("Witch")
    
    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, [character], locations)  # Pass the selected character
    game.start()


if __name__ == '__main__':
    start_game()