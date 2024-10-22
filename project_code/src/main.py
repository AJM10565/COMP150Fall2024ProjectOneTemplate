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
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        # Add more stats as needed

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence]  # Extend this list if there are more stats


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
        print("Game Over.")

    def check_game_over(self):
        return self.correct_answers >= 3  # End game after 3 correct answers

    def visit_shops(self):
        shop_choice = input("Would you like to visit the Weapon Shop or Upgrade Shop? (weapon/upgrade/none): ").lower()
        if shop_choice == "weapon":
            weapon_shop = WeaponShop()
            weapon_shop.purchase_weapon(self.party[0])  # First character buys weapon
        elif shop_choice == "upgrade":
            upgrade_shop = UpgradeShop()
            upgrade_shop.purchase_upgrade(self.party[0])  # First character upgrades stats
        else:
            print("Skipping shops.")

    def final_encounter(self):
        print("Now it's time to battle Mr. Krabs!")
        player = self.party[0]  # Assuming a single player character for now

        krabs_health = 30
        while krabs_health > 0 and player.health > 0:
            print(f"Mr. Krabs has {krabs_health} health. You have {player.health} health.")
            attack_choice = input("Where would you like to attack Mr. Krabs? (torso/arms/legs): ").lower()

            if attack_choice == "torso":
                damage = random.randint(5, 10) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice == "arms":
                damage = random.randint(1, 5) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice == "legs":
                damage = random.randint(1, 5) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            else:
                print("Invalid attack choice.")
                continue

            # Mr. Krabs strikes back
            krabs_damage = random.randint(1, 5)
            player.health -= krabs_damage
            print(f"Mr. Krabs hit you for {krabs_damage} damage!")

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
        elif krabs_health <= 0:
            print("Mr. Krabs has been defeated! You win!")


class Parser:
    def select_party_member(self, party: List[Character]) -> Character:
        return party[0]  # Simplified for now; could allow selection based on user input

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
