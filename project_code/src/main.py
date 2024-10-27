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
        self.weapon = "None"

    def collect_krabby_patties(self, amount: int):
        self.krabby_patties += amount
        self.health = self.krabby_patties  # Update health based on Krabby Patties
        print(f"{self.name} collected {amount} Krabby Patties! Total: {self.krabby_patties}. Health is now: {self.health}")

    def spend_krabby_patties(self, amount: int):
        if self.krabby_patties >= amount:
            self.krabby_patties -= amount
            self.health = self.krabby_patties  # Update health after spending
            return True
        else:
            print(f"Not enough Krabby Patties! {self.name} has {self.krabby_patties}, but {amount} is needed.")
            return False

    def __str__(self):
        return f"Character: {self.name}, Health: {self.health}, Strength: {self.strength}, Krabby Patties: {self.krabby_patties}, Weapon: {self.weapon}"


class WeaponShop:
    def __init__(self):
        self.weapons = {
            "Spatula": 5,
            "Karen": 10,
            "Golden Spatula": 20
        }

    def display_weapons(self):
        print("Weapons available for purchase:")
        for index, (weapon, cost) in enumerate(self.weapons.items()):
            print(f"{index + 1}. {weapon}: {cost} Krabby Patties")

    def purchase_weapon(self, character: Character):
        self.display_weapons()
        choice = input("Choose a weapon by number: ")
        
        try:
            weapon_choice_index = int(choice) - 1
            weapon_choice = list(self.weapons.keys())[weapon_choice_index]
            cost = self.weapons[weapon_choice]
            if character.spend_krabby_patties(cost):
                character.weapon = weapon_choice
                print(f"{character.name} purchased {weapon_choice}!")
            else:
                print("Transaction failed. Not enough Krabby Patties.")
        except (ValueError, IndexError):
            print("Invalid choice.")


class UpgradeShop:
    def __init__(self):
        self.upgrades = {
            "Strength Upgrade": 5,
            "Health Upgrade": 5
        }

    def display_upgrades(self):
        print("Upgrades available for purchase:")
        for index, (upgrade, cost) in enumerate(self.upgrades.items()):
            print(f"{index + 1}. {upgrade}: {cost} Krabby Patties")

    def purchase_upgrade(self, character: Character):
        self.display_upgrades()
        choice = input("Choose an upgrade by number: ")
        
        try:
            upgrade_choice_index = int(choice) - 1
            upgrade_choice = list(self.upgrades.keys())[upgrade_choice_index]
            if upgrade_choice == "Strength Upgrade":
                if character.spend_krabby_patties(self.upgrades[upgrade_choice]):
                    character.strength.modify(5)
                    print(f"{character.name}'s strength increased to {character.strength.value}!")
            elif upgrade_choice == "Health Upgrade":
                if character.spend_krabby_patties(self.upgrades[upgrade_choice]):
                    character.health += 10
                    print(f"{character.name}'s health increased to {character.health}!")
            else:
                print("Invalid choice.")
        except (ValueError, IndexError):
            print("Invalid choice.")


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
            return self.ask_riddle(parser)  # Return the reward directly

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)
        return 0  # No reward if no riddle is asked

    def ask_riddle(self, parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)

        if user_choice == self.correct_answer:
            print("You solved the riddle and pushed the door open. You may proceed.")
            self.status = EventStatus.PASS
            return 25  # Return 25 Krabby Patties for a correct answer
        else:
            print("Wrong answer! The door remains closed.")
            self.status = EventStatus.FAIL
            return 0  # No reward for a wrong answer

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
            reward = event.execute(self.party, self.parser)
            if reward > 0:
                for character in self.party:
                    character.collect_krabby_patties(reward)  # Each character gets the reward

            if event.status == EventStatus.PASS:
                self.collect_krabby_patties()  # Collect Krabby Patties
                self.ask_second_riddle()  # Proceed to a second riddle
            if self.check_game_over():
                self.continue_playing = False
        self.visit_shops()  # Allow player to visit shops before final boss
        self.final_encounter()  # Fight Mr. Krabs after all events
        print("Game Over.")

    def collect_krabby_patties(self, amount: int = 0):
        for character in self.party:
            if amount > 0:
                character.collect_krabby_patties(amount)
            else:
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
        
        if user_choice == second_riddle['correct_answer']:
            print("You solved the second riddle! You may proceed.")
            self.collect_krabby_patties(25)  # Give 25 Krabby Patties
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

        if user_choice == third_riddle['correct_answer']:
            print("You solved the third riddle! You may proceed.")
            self.collect_krabby_patties(25)  # Give 25 Krabby Patties
            self.correct_answers += 1  # Increment correct answer count
        else:
            print("Wrong answer! You cannot proceed.")

    def check_game_over(self):
        return self.correct_answers >= 3  # End game after 3 correct answers

    def visit_shops(self):
        shop_choice = input("Would you like to visit the Weapon Shop or Upgrade Shop? (weapon/upgrade/none): ").lower()
        if shop_choice == "weapon":
            weapon_shop = WeaponShop()
            weapon_shop.purchase_weapon(self.parser.select_party_member(self.party))  # Chosen character buys weapon
        elif shop_choice == "upgrade":
            upgrade_shop = UpgradeShop()
            upgrade_shop.purchase_upgrade(self.parser.select_party_member(self.party))  # Chosen character upgrades stats
        else:
            print("Skipping shops.")

    def final_encounter(self):
        print("Now it's time to battle Mr. Krabs!")
        player = self.parser.select_party_member(self.party)  # Let the player choose their character

        krabs_health = 80  # Set Mr. Krabs' initial health to 80
        while krabs_health > 0 and player.health > 0:
            print(f"Mr. Krabs has {krabs_health} health. You have {player.health} health.")
            attack_choice = input("Where would you like to attack Mr. Krabs? (1: Torso, 2: Arms, 3: Legs): ").lower()

            if attack_choice == "1":
                damage = random.randint(5, 10) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice == "2":
                damage = random.randint(1, 5) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice == "3":
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
        print("Choose your character:")
        for index, character in enumerate(party):
            print(f"{index + 1}. {character.name}")
        user_input = input("Select a character by number: ")
        
        try:
            choice_index = int(user_input) - 1
            if 0 <= choice_index < len(party):
                return party[choice_index]
            else:
                print("Invalid choice. Please choose a valid number.")
                return self.select_party_member(party)  # Retry if invalid
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.select_party_member(party)  # Retry if invalid

    def select_stat(self, character: Character) -> Statistic:
        return character.strength  # Simplified; could allow user to choose between stats

    def select_riddle_option(self, options: List[str]) -> int:
        print("Options:")
        for index, option in enumerate(options):
            print(f"{index}: {option}")
        user_input = input("Choose the number corresponding to your answer: ")
        
        try:
            choice_index = int(user_input)
            if 0 <= choice_index < len(options):
                return choice_index
            else:
                print("Invalid choice. Please choose a valid number.")
                return self.select_riddle_option(options)  # Retry if invalid
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.select_riddle_option(options)  # Retry if invalid


def main():
    parser = Parser()

    # Example character setup
    spongebob = Character(name="SpongeBob", health=100, strength=10)
    patrick = Character(name="Patrick", health=100, strength=8)
    plankton = Character(name="Plankton", health=80, strength=12)
    squidward = Character(name="Squidward", health=90, strength=9)

    # Create a party with all characters
    characters = [spongebob, patrick, plankton, squidward]

    # Example location setup with events
    location1 = Location(events=[
        Event({
            'primary_attribute': 'Strength',
            'secondary_attribute': 'Agility',
            'riddle_question': 'What has to be broken before you can use it?',
            'riddle_options': ['Egg', 'Window', 'Lock'],
            'correct_answer': 0
        })
    ])

    game = Game(parser, characters, [location1])
    game.start()


if __name__ == "__main__":
    main()
