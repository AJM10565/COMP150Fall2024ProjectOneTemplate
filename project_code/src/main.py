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
        self.has_secret_formula = False

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
            "1. Spatula": 5,
            "2. Karen": 10,
            "3. Golden Spatula": 20
        }

    def display_weapons(self):
        print("Weapons available for purchase:")
        for index, (weapon, cost) in enumerate(self.weapons.items()):
            print(f"{index + 1}. {weapon}: {cost} Krabby Patties")

    def purchase_weapon(self, character: Character):
        self.display_weapons()
<<<<<<< HEAD
        choice = input("Choose a weapon by number: ")
        
        try:
            weapon_choice_index = int(choice) - 1
            weapon_choice = list(self.weapons.keys())[weapon_choice_index]
            cost = self.weapons[weapon_choice]
=======
        weapon_choice = input("Enter the number of the weapon you would like to buy (1-3): ")
        weapon_map = {
            "1": "1. Spatula",
            "2": "2. Karen",
            "3": "3. Golden Spatula"
        }
        if weapon_choice in weapon_map:
            weapon_name = weapon_map[weapon_choice]
            cost = self.weapons[weapon_name]
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
            if character.spend_krabby_patties(cost):
                character.weapon = weapon_name
                print(f"{character.name} purchased {weapon_name}!")
            else:
                print("Transaction failed. Not enough Krabby Patties.")
        except (ValueError, IndexError):
            print("Invalid choice.")


class UpgradeShop:
    def __init__(self):
        self.upgrades = {
            "1. Strength Upgrade": 5,
            "2. Health Upgrade": 5
        }

    def display_upgrades(self):
        print("Upgrades available for purchase:")
        for index, (upgrade, cost) in enumerate(self.upgrades.items()):
            print(f"{index + 1}. {upgrade}: {cost} Krabby Patties")

    def purchase_upgrade(self, character: Character):
        self.display_upgrades()
<<<<<<< HEAD
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
=======
        upgrade_choice = input("Enter the number of the upgrade you would like to buy (1-2): ")
        upgrade_map = {
            "1": "1. Strength Upgrade",
            "2": "2. Health Upgrade"
        }
        if upgrade_choice in upgrade_map:
            upgrade_name = upgrade_map[upgrade_choice]
            if character.spend_krabby_patties(self.upgrades[upgrade_name]):
                if upgrade_choice == "1":
                    character.strength.modify(5)
                    print(f"{character.name}'s strength increased to {character.strength.value}!")
                else:
                    character.health += 10
                    print(f"{character.name}'s health increased to {character.health}!")
        else:
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
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
<<<<<<< HEAD
            return self.ask_riddle(parser)  # Return the reward directly
=======
            self.ask_riddle(parser)
            return
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)
        return 0  # No reward if no riddle is asked

    def ask_riddle(self, parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)
<<<<<<< HEAD

        if user_choice == self.correct_answer:
=======
        
        if user_choice.isdigit() and 0 <= int(user_choice)-1 < len(self.riddle_options) and int(user_choice)-1 == self.correct_answer:
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
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
        self.correct_answers = 0
        self.used_riddles = set()
        self.all_riddles = [
            {
                "riddle_question": "What has to be broken before you can use it?",
                "riddle_options": ["1. Egg", "2. Window", "3. Lock"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What has keys, but no locks; space, but no room; and you can enter, but not go in?",
                "riddle_options": ["1. A keyboard", "2. A map", "3. A phone"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What gets wetter and wetter the more it dries?",
                "riddle_options": ["1. A towel", "2. A sponge", "3. A cloth"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What has a head and a tail but no body?",
                "riddle_options": ["1. A coin", "2. A snake", "3. A worm"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What is full of holes but still holds water?",
                "riddle_options": ["1. A sponge", "2. A bucket", "3. A bottle"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What can travel around the world while staying in a corner?",
                "riddle_options": ["1. A stamp", "2. A globe", "3. A map"],
                "correct_answer": 0
            },
            {
                "riddle_question": "What has cities, but no houses; forests, but no trees; and rivers, but no water?",
                "riddle_options": ["1. A map", "2. A globe", "3. A picture"],
                "correct_answer": 0
            }
        ]

    def get_unused_riddle(self):
        available_riddles = [riddle for i, riddle in enumerate(self.all_riddles) 
                           if i not in self.used_riddles]
        if not available_riddles:
            return None
        
        riddle_index = self.all_riddles.index(random.choice(available_riddles))
        self.used_riddles.add(riddle_index)
        return self.all_riddles[riddle_index]

    def start(self):
        while self.continue_playing:
<<<<<<< HEAD
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
=======
            riddle = self.get_unused_riddle()
            if not riddle:
                print("\nYou've solved all available riddles!")
                self.choose_path()
                break

            print("\n" + riddle['riddle_question'])
            for option in riddle['riddle_options']:
                print(option)
            
            user_choice = input("Enter the number of your answer (1-3): ")
            if user_choice.isdigit() and int(user_choice)-1 == riddle['correct_answer']:
                print("Correct! You've earned more Krabby Patties!")
                self.collect_krabby_patties()
                self.correct_answers += 1
            else:
                print("Wrong answer!")

            if self.correct_answers >= 3:
                self.choose_path()
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)

    def collect_krabby_patties(self, amount: int = 0):
        for character in self.party:
<<<<<<< HEAD
            if amount > 0:
                character.collect_krabby_patties(amount)
            else:
                amount = random.randint(1, 5)  # Randomly collect between 1 and 5 Krabby Patties
                character.collect_krabby_patties(amount)
=======
            amount = random.randint(1, 5)
            character.collect_krabby_patties(amount)
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)

    def choose_path(self):
        while True:  # Loop to allow multiple actions until the final choice
            print("\nYou've proven your worth! What would you like to do?")
            print("1. Fight Mr. Krabs")
            print("2. Continue solving riddles for more Krabby Patties")
            print("3. Visit shops")
            print("4. End game")
        
            choice = input("Enter your choice (1-4): ")
        
<<<<<<< HEAD
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
=======
            if choice == "1":
                self.visit_shops()  # Option to shop before final battle
                self.final_encounter()
                self.continue_playing = False
                break
            elif choice == "2":
                if len(self.used_riddles) < len(self.all_riddles):
                    print("Continuing with more riddles...")
                    self.correct_answers = 0
                    break  # Continue to solve riddles
                else:
                    print("No more riddles available! Time to face Mr. Krabs!")
                    self.visit_shops()  # Option to shop before final battle
                    self.final_encounter()
                    self.continue_playing = False
                break
            elif choice == "3":
                self.visit_shops()  # Visit shops but keep playing
            elif choice == "4":
                self.continue_playing = False
                print("Ending game. Thanks for playing!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)

    # Adjusted `visit_shops` method (moved out of `choose_path`)
    def visit_shops(self):
        print("\nWould you like to visit a shop?")
        print("1. Weapon Shop")
        print("2. Upgrade Shop")
        print("3. Skip shopping")
    
        shop_choice = input("Enter your choice (1-3): ")
        if shop_choice == "1":
            weapon_shop = WeaponShop()
<<<<<<< HEAD
            weapon_shop.purchase_weapon(self.parser.select_party_member(self.party))  # Chosen character buys weapon
        elif shop_choice == "upgrade":
            upgrade_shop = UpgradeShop()
            upgrade_shop.purchase_upgrade(self.parser.select_party_member(self.party))  # Chosen character upgrades stats
=======
            weapon_shop.purchase_weapon(self.party[0])
        elif shop_choice == "2":
            upgrade_shop = UpgradeShop()
            upgrade_shop.purchase_upgrade(self.party[0])
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
        else:
            print("Skipping shops.")

    def display_secret_formula(self):
        print("\n🌟 CONGRATULATIONS! You've obtained the Secret Krabby Patty Formula! 🌟")
        print("\nThe Secret Formula contains:")
        print("- A pinch of King Neptune's Poseidon Powder")
        print("- Two tablespoons of underwater love")
        print("- Three cups of crushed coral")
        print("- A dash of whale song")
        print("- Secret underwater herbs and spices")
        print("- And most importantly... a sprinkle of friendship!")
        print("\nMr. Krabs whispers: 'Use it wisely, me boy!'")
        
    def final_encounter(self):
        print("\n🦀 FINAL BOSS BATTLE: Mr. Krabs 🦀")
        print("Now it's time to battle Mr. Krabs!")
<<<<<<< HEAD
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
=======
        player = self.party[0]
        krabs_health = 150
        while krabs_health > 0 and player.health > 0:
            print(f"\nMr. Krabs has {krabs_health} health. You have {player.health} health.")
            print("Where would you like to attack Mr. Krabs?")
            print("1. Torso")
            print("2. Arms")
            print("3. Legs")
            
            attack_choice = input("Enter your choice (1-3): ")
            
            if attack_choice == "1":
                damage = random.randint(10, 20) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice in ["2", "3"]:
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
                damage = random.randint(1, 5) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            else:
                print("Invalid attack choice.")
                continue

            if krabs_health > 0:
                krabs_damage = random.randint(1, 5)
                player.health -= krabs_damage
                print(f"Mr. Krabs hit you for {krabs_damage} damage!")

        if player.health <= 0:
            print(f"\n💔 {player.name} has been defeated by Mr. Krabs!")
            print("Game Over! Better luck next time!")
        elif krabs_health <= 0:
            print("\n🎉 Victory! You've defeated Mr. Krabs!")
            player.has_secret_formula = True
            self.display_secret_formula()
            print(f"\nFinal Stats:")
            print(f"Health Remaining: {player.health}")
            print(f"Krabby Patties Collected: {player.krabby_patties}")
            print(f"Weapon Used: {player.weapon}")
            print(f"Total Riddles Solved: {len(self.used_riddles)}")
            print("\nThanks for playing! The End! 🎮")



class Parser:
    def select_party_member(self, party: List[Character]) -> Character:
<<<<<<< HEAD
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
=======
        return party[0]
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)

    def select_stat(self, character: Character) -> Statistic:
        return character.strength

<<<<<<< HEAD
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
=======
    def select_riddle_option(self, options: List[str]) -> str:
        for i, option in enumerate(options, 1):
            print(option)
        return input("Enter the number of your answer (1-3): ")
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)


def main():
    parser = Parser()
    spongebob = Character(name="SpongeBob", health=100, strength=10)
<<<<<<< HEAD
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
=======
    
    # Example event data with necessary keys
    event_data = {
        "primary_attribute": "Strength",
        "secondary_attribute": "Health",
        "riddle_question": "What has to be broken before you can use it?",
        "riddle_options": ["1. Egg", "2. Window", "3. Lock"],
        "correct_answer": 0
    }
    
    # Create a location with this event
    location1 = Location(events=[Event(event_data)])
    game = Game(parser, [spongebob], [location1])
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
    game.start()



if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> a4b126e (Fixed some bugs within the fighting, Krabs has increased health, now have an option to fight or keep earning and can solve more riddles, stats given at the end of the game. Want to work on inreasing Krab's damage and make the game more difficult and detailed.)
