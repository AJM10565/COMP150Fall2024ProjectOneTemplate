import json
import random
from typing import List
from enum import Enum


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


class Character:
    def __init__(self, name: str, health: int = 100, strength: int = 10):
        self.name = name
        self.health = health
        self.strength = Statistic("Strength", value=strength, description="Strength is a measure of physical power.")
        self.krabby_patties = 0

    def collect_krabby_patties(self, amount: int):
        self.krabby_patties += amount
        print(f"{self.name} collected {amount} Krabby Patties! Total: {self.krabby_patties}")

    def __str__(self):
        return f"Character: {self.name}, Health: {self.health}, Strength: {self.strength}, Krabby Patties: {self.krabby_patties}"


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.riddle_question = data.get('riddle_question', '')
        self.riddle_options = data.get('riddle_options', [])
        self.correct_answer = data.get('correct_answer', -1)
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        if self.riddle_question:
            self.ask_riddle(parser)
            return  # End execution after riddle handling

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def ask_riddle(self, parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)
        
        if self.riddle_options.index(user_choice) == self.correct_answer:
            print("You solved the riddle and pushed the door open. You may proceed.")
            self.status = EventStatus.PASS
        else:
            print("Wrong answer! The door remains closed.")
            self.status = EventStatus.FAIL

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print("You successfully used your strength!")
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print("You made some progress, but not enough!")
        else:
            self.status = EventStatus.FAIL
            print("You failed to achieve your goal.")


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
        self.correct_answers = 0  # Track the number of correct answers

    def start(self):
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if event.status == EventStatus.PASS:
                self.collect_krabby_patties()  # Collect Krabby Patties
                self.correct_answers += 1  # Increment correct answer count
                self.ask_second_riddle()  # Proceed to a second riddle
            if self.check_game_over():
                self.continue_playing = False
        self.final_encounter()  # Fight Mr. Krabs after all events
        print("Game Over.")

    def collect_krabby_patties(self):
        for character in self.party:
            amount = random.randint(1, 5)  # Randomly collect between 1 and 5 Krabby Patties
            character.collect_krabby_patties(amount)

    def ask_second_riddle(self):
        second_riddle = {
            "riddle_question": "What is always in front of you but can’t be seen?",
            "riddle_options": [
                "The future",
                "A wall",
                "Your nose"
            ],
            "correct_answer": 0  # First option is the correct answer
        }
        
        print(second_riddle['riddle_question'])
        user_choice = self.parser.select_riddle_option(second_riddle['riddle_options'])
        
        if second_riddle['riddle_options'].index(user_choice) == second_riddle['correct_answer']:
            print("You solved the second riddle! You may proceed.")
            self.correct_answers += 1  # Increment correct answer count
            self.ask_third_riddle()  # Proceed to the third riddle
        else:
            print("Wrong answer! You cannot proceed.")

    def ask_third_riddle(self):
        third_riddle = {
            "riddle_question": "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
            "riddle_options": [
                "An echo",
                "A cloud",
                "A shadow"
            ],
            "correct_answer": 0  # First option is the correct answer
        }

        print(third_riddle['riddle_question'])
        user_choice = self.parser.select_riddle_option(third_riddle['riddle_options'])

        if third_riddle['riddle_options'].index(user_choice) == third_riddle['correct_answer']:
            print("You solved the third riddle! You may proceed to face Mr. Krabs.")
            self.final_encounter()  # Proceed to fight Mr. Krabs
        else:
            print("Wrong answer! You cannot proceed.")

    def final_encounter(self):
        print("You open the door and see Mr. Krabs!")
        
        # Distribute Krabby Patties based on correct answers
        for character in self.party:
            if character.name != "Patrick Star":
                character.collect_krabby_patties(10 * self.correct_answers)  # Each correct answer gives 10 Krabby Patties

        character = self.parser.select_party_member(self.party)
        weapon = self.select_weapon(character)
        print(f"{character.name} chooses to fight Mr. Krabs with a {weapon}!")
        
        self.fight_mr_krabs(character, weapon)

    def select_weapon(self, character: Character) -> str:
        weapons = ["Spatula", "Karen", "Kelp"]
        print("Choose a weapon:")
        for idx, weapon in enumerate(weapons):
            print(f"{idx + 1}. {weapon}")
        choice = int(self.parser.parse("Enter the number of your chosen weapon: ")) - 1
        return weapons[choice]

    def fight_mr_krabs(self, character: Character, weapon: str):
        print("A wild Mr. Krabs appears! Prepare for battle!")
        
        # Calculate total strength based on Krabby Patties collected
        total_strength = character.strength.value + character.krabby_patties
        print(f"Your total strength with {weapon} is: {total_strength}")

        consecutive_hits = {'legs': 0, 'arms': 0, 'torso': 0}

        while True:
            print("\nChoose a part to hit:")
            print("1. Torso")
            print("2. Left Arm")
            print("3. Right Arm")
            print("4. Left Leg")
            print("5. Right Leg")
            choice = int(self.parser.parse("Enter the number of the part to hit: ")) - 1
            
            if choice == 0:  # Torso
                consecutive_hits['torso'] += 1
                if consecutive_hits['torso'] == 2:
                    print("You hit Mr. Krabs' torso twice! You die and return to the riddle screen.")
                    return  # End the fight and return to riddles
                print("You hit Mr. Krabs' torso! Ouch! You lose some health.")
                character.health -= 10  # Deduct health for hitting torso
                consecutive_hits['legs'] = 0
                consecutive_hits['arms'] = 0
                
            elif choice in (1, 2):  # Arms
                consecutive_hits['arms'] += 1
                print("You hit Mr. Krabs' arm!")
                if consecutive_hits['arms'] == 2:
                    print("You hit both of Mr. Krabs' arms twice! You win!")
                    print(f"Congratulations! {character.name} has defeated Mr. Krabs and obtained the Krabby Patty secret formula!")
                    self.continue_playing = False  # End the game
                    return
                
                print("You hit Mr. Krabs' arm! But you lose some health.")
                character.health -= 5  # Deduct health for hitting arm
                consecutive_hits['torso'] = 0
                consecutive_hits['legs'] = 0
                
            elif choice in (3, 4):  # Legs
                consecutive_hits['legs'] += 1
                print("You hit Mr. Krabs' leg!")
                if consecutive_hits['legs'] == 2:
                    print("You hit both of Mr. Krabs' legs twice! You win!")
                    print(f"Congratulations! {character.name} has defeated Mr. Krabs and obtained the Krabby Patty secret formula!")
                    self.continue_playing = False  # End the game
                    return
                
                print("You hit Mr. Krabs' leg! But you lose some health.")
                character.health -= 5  # Deduct health for hitting leg
                consecutive_hits['torso'] = 0
                consecutive_hits['arms'] = 0
                
            else:
                print("Invalid choice! Please try again.")

            # Check if character is still alive
            if character.health <= 0:
                print(f"{character.name} has been defeated by Mr. Krabs! Returning to the riddle screen.")
                return

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
        stats = [character.strength]  # Assuming only strength is relevant
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]

    def select_riddle_option(self, options: List[str]) -> str:
        print("Choose an answer to the riddle:")
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")
        choice = int(self.parse("Enter the number of your answer: ")) - 1
        return options[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()

    characters_dict = {
        "spongebob": ("SpongeBob SquarePants", 120, 15),
        "patrick": ("Patrick Star", 150, 10),
        "pearl": ("Pearl Krabs", 100, 12),
        "plankton": ("Plankton", 80, 8),
        "squidward": ("Squidward Tentacles", 90, 10),
        "mrkrabs": ("Mr. Krabs", 150, 20)  # Added Mr. Krabs to the list of characters
    }


    characters = []
    for key, (name, health, strength) in characters_dict.items():
        characters.append(Character(name, health, strength))

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()



