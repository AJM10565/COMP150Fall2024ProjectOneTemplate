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


import random
from typing import List

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
            # Quick fight event with choices
            print("A wild creature appears and attacks you!")
            choice = self.parser.parse("Choose your action: 1. Attack directly  2. Attempt to dodge (Choose 1 or 2): ")

            if choice == "1":
                # Direct attack with a possible reward but higher risk
                outcome = random.choice(["win", "lose_health", "lose"])
                if outcome == "win":
                    print("You bravely fought and defeated the enemy! You continue your journey.")
                elif outcome == "lose_health":
                    for character in self.party:
                        character.take_damage(15)  # Example health loss for partial loss
                    print("You fought bravely but took some damage.")
                elif outcome == "lose":
                    print("You lost the fight and suffered a heavy setback.")
                    self.continue_playing = False  # Ends game if losing is game-ending

            elif choice == "2":
                # Dodging has a lower risk of major damage but with no chance to "win"
                outcome = random.choice(["dodge_success", "dodge_fail"])
                if outcome == "dodge_success":
                    print("You successfully dodged the enemy's attacks and avoided damage!")
                elif outcome == "dodge_fail":
                    for character in self.party:
                        character.take_damage(10)  # Example health loss for failed dodge
                    print("You tried to dodge but got hit and took some damage.")

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
        # Scenario setup for the final event
        final_event = {
            "prompt_text": "You find a glowing ruby resting on a stone pedestal in the woods. Do you destroy it or take it?",
            "choices": [
                {"text": "Destroy the ruby and end Halloween night", "outcome": "destroy"},
                {"text": "Take the ruby for yourself", "outcome": "take_ruby"}
            ]
        }

        # Display the prompt
        print(final_event["prompt_text"])
        print("1: Destroy the ruby and end Halloween night")
        print("2: Take the ruby for yourself")

        # Get the choice
        choice = self.parser.parse("Choose an option (1 or 2): ")

        # Execute the code based on the selected choice
        if choice == "1":
            print("You see the fog clearing up! You have saved Halloween Night. Congratulations!")
            self.continue_playing = False  # This option ends the game
        elif choice == "2":
            print("The ruby sears your hand and a powerful beast summons and knocks you out cold! Greed is never the answer...")
            
            # For simplicity's sake, we’ll loop back to the beginning
            self.current_quest = 0
            print("You feel a strange energy transporting you back to the beginning of your journey...")


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