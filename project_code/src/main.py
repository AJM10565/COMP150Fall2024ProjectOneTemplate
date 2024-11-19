
import json
import os
import random
from typing import List
from enum import Enum
from flask import Flask, request, jsonify
import gunicorn  # Import gunicorn
from flask import Flask, render_template 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render your main HTML template

# ... rest of your Flask app routes ...
app = Flask(__name__)

# ... your Flask app routes and code ...
# Ive changed nothing here you are
@app.route('/start', methods=['POST'])
def start():
    # Your existing code
    return jsonify({"message": "Game started! Good luck in Bikini Bottom!"})

@app.route('/next', methods=['POST'])
def next_step():
    # Your existing code
    return jsonify({"message": "Next step triggered! Check the console for progress."})

@app.route('/choice', methods=['POST'])
def make_choice():
    # Your existing code
    return jsonify({"message": f"Choice {choice} registered!"})

# ... rest of your code ...

if __name__ == '__main__':
    app.run(debug=True)  # Keep this for development

# For production, use Gunicorn:

    # Set the worker class, number of workers, and the Python module and app
    gunicorn_opts = {
        'workers': 3,  # Adjust the number of workers as needed
        'bind': '0.0.0.0:5000',  # Listen on all interfaces
        'worker_class':                 'uvicorn.workers.UvicornWorker', # Optionally use Uvicorn workers
        'accesslog': '-',
        'errorlog': '-'
    }
    gunicorn.run(
        'main:app',
        **gunicorn_opts
    )
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
        print(f"{self.name} collected {amount} Krabby Patties! Total: {self.krabby_patties}")

    def spend_krabby_patties(self, amount: int):
        if self.krabby_patties >= amount:
            self.krabby_patties -= amount
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
        for weapon, cost in self.weapons.items():
            print(f"{weapon}: {cost} Krabby Patties")

    def purchase_weapon(self, character: Character):
        self.display_weapons()
        weapon_choice = input("Enter the number of the weapon you would like to buy (1-3): ")
        weapon_map = {
            "1": "1. Spatula",
            "2": "2. Karen",
            "3": "3. Golden Spatula"
        }
        if weapon_choice in weapon_map:
            weapon_name = weapon_map[weapon_choice]
            cost = self.weapons[weapon_name]
            if character.spend_krabby_patties(cost):
                character.weapon = weapon_name
                print(f"{character.name} purchased {weapon_name}!")
            else:
                print("Transaction failed. Not enough Krabby Patties.")
        else:
            print("Invalid choice.")


class UpgradeShop:
    def __init__(self):
        self.upgrades = {
            "1. Strength Upgrade": 5,
            "2. Health Upgrade": 5
        }

    def display_upgrades(self):
        print("Upgrades available for purchase:")
        for upgrade, cost in self.upgrades.items():
            print(f"{upgrade}: {cost} Krabby Patties")

    def purchase_upgrade(self, character: Character):
        self.display_upgrades()
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
            print("Invalid choice.")


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.riddle_question = data.get('riddle_question', '')
        self.riddle_options = data.get('riddle_options', [])
        self.correct_answer = data.get('correct_answer', -1)
        self.status = EventStatus.UNKNOWN

        # Randomize the riddle options and update the correct answer index
        self.shuffle_riddle_options()

    def shuffle_riddle_options(self):
        # If there are no options or only one, we don't need to shuffle
        if len(self.riddle_options) > 1:
            # Randomly shuffle the riddle options
            correct_option = self.riddle_options[self.correct_answer]  # Save the correct answer
            random.shuffle(self.riddle_options)  # Shuffle all options

            # After shuffling, find the new index of the correct answer
            self.correct_answer = self.riddle_options.index(correct_option)

    def execute(self, party: List[Character], parser):
        if self.riddle_question:
            self.ask_riddle(parser)
            return

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def ask_riddle(self, parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)

        if user_choice.isdigit() and 0 <= int(user_choice)-1 < len(self.riddle_options) and int(user_choice)-1 == self.correct_answer:
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

class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.riddle_question = data.get('riddle_question', '')
        self.riddle_options = data.get('riddle_options', [])
        self.correct_answer = data.get('correct_answer', -1)
        self.status = EventStatus.UNKNOWN

        # Randomize the riddle options and update the correct answer index
        self.shuffle_riddle_options()

    def shuffle_riddle_options(self):
        # If there are no options or only one, we don't need to shuffle
        if len(self.riddle_options) > 1:
            # Randomly shuffle the riddle options
            correct_option = self.riddle_options[self.correct_answer]  # Save the correct answer
            random.shuffle(self.riddle_options)  # Shuffle all options

            # After shuffling, find the new index of the correct answer
            self.correct_answer = self.riddle_options.index(correct_option)

    def execute(self, party: List[Character], parser):
        if self.riddle_question:
            self.ask_riddle(parser)
            return

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def ask_riddle(self, parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)

        if user_choice.isdigit() and 0 <= int(user_choice)-1 < len(self.riddle_options) and int(user_choice)-1 == self.correct_answer:
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


class SandyCheeks(Character):
    def __init__(self):
        super().__init__(name="Sandy Cheeks", health=120, strength=15)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.correct_answers = 0
        self.used_riddles = set()

        # Load riddles from JSON file
        # Load riddles from JSON file located in the 'data' directory
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'riddles.json')
        with open(data_path, 'r') as file:
            self.all_riddles = json.load(file)

    def introduce_game(self):
        print("\n🌟 Welcome to Bikini Bottom! 🌟")
        print("Answer riddles to collect Krabby Patties and earn points to upgrade and choose your weapons.")
        print("Defeat Sandy Cheeks and Mr. Krabs to steal the Krabby Patty secret formula and win the game!")
        print("\nGood luck, and watch out for traps and tricky riddles along the way!\n")

    def get_unused_riddle(self):
        available_riddles = [riddle for i, riddle in enumerate(self.all_riddles) 
                           if i not in self.used_riddles]
        if not available_riddles:
            return None

        riddle_index = self.all_riddles.index(random.choice(available_riddles))
        self.used_riddles.add(riddle_index)
        return self.all_riddles[riddle_index]

    def start(self):
        # Call the game introduction here
        self.introduce_game()

        while self.continue_playing:
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

    def collect_krabby_patties(self):
        for character in self.party:
            amount = random.randint(1, 5)
            character.collect_krabby_patties(amount)

    def choose_path(self):
        while True:  # Loop to allow multiple actions until the final choice
            print("\nYou've proven your worth! What would you like to do?")
            print("1. Fight Mr. Krabs")
            print("2. Continue solving riddles for more Krabby Patties")
            print("3. Visit shops")
            print("4. End game")

            choice = input("Enter your choice (1-4): ")

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

    # Adjusted visit_shops method (moved out of choose_path)
    def visit_shops(self):
        print("\nWould you like to visit a shop?")
        print("1. Weapon Shop")
        print("2. Upgrade Shop")
        print("3. Skip shopping")

        shop_choice = input("Enter your choice (1-3): ")
        if shop_choice == "1":
            weapon_shop = WeaponShop()
            weapon_shop.purchase_weapon(self.party[0])
        elif shop_choice == "2":
            upgrade_shop = UpgradeShop()
            upgrade_shop.purchase_upgrade(self.party[0])
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
    def display_defeat_dialogue(self):
        print("\nMr. Krabs stands over you, a smirk on his face.")
        print("Mr. Krabs: 'Ye thought ye could take me secret formula? Ha! Not a chance, me boy!'")
        print("Mr. Krabs: 'This formula is me life! No one shall take it from me, not even a sponge like ye!'")
        print("Mr. Krabs: 'Now get back to work, or I'll have ye scrubbing the floors!'")


    def talk_to_mr_krabs(self):
        print("\nMr. Krabs: 'So, ye think ye can just waltz in here and take me secret formula, eh?'")
        print("Mr. Krabs: 'Why should I let ye? What's yer plan?'")

        while True:
            print("1. I want to betray you and take the formula!")
            print("2. I just wanted to see the formula for myself.")
            print("3. I think you should share it with me!")
            print("4. I was just kidding, I love the Krabby Patty!")

            response = input("Choose your response (1-4): ")

            if response == "1":
                print("Mr. Krabs: 'Betray me? Ye scallywag! I'll make sure ye regret that!'")
                break
            elif response == "2":
                print("Mr. Krabs: 'Curiosity killed the cat, ya know! What makes ye think I'm gonna show ye?'")
                break
            elif response == "3":
                print("Mr. Krabs: 'Share it? Over me dead body!'")
                break
            elif response == "4":
                print("Mr. Krabs: 'Aye, that's what I like to hear! But ye still can't have it!'")
                break
            else:
                print("Invalid choice. Please select a valid option.")




    def final_encounter(self):
        print("\n🦊 BOSS BATTLE: Sandy Cheeks 🦊")
        sandy = SandyCheeks()

        player = self.party[0]
        sandy_health = sandy.health
        sandy_health = 75

        while sandy_health > 0 and player.health > 0:
            print(f"\nSandy Cheeks has {sandy_health} health. You have {player.health} health.")
            print("Where would you like to attack Sandy?")
            print("1. Head")
            print("2. Tail")
            print("3. Paws")

            attack_choice = input("Enter your choice (1-3): ")

            if attack_choice == "1":
                damage = random.randint(10, 20) + player.strength.value
                sandy_health -= damage
                print(f"You dealt {damage} damage to Sandy Cheeks!")
            elif attack_choice in ["2", "3"]:
                damage = random.randint(5, 15) + player.strength.value
                sandy_health -= damage
                print(f"You dealt {damage} damage to Sandy Cheeks!")
            else:
                print("Invalid attack choice.")
                continue

            if sandy_health > 0:
                sandy_damage = random.randint(2, 5) + sandy.strength.value  # Reduced Sandy's attack strength
                player.health -= sandy_damage
                print(f"Sandy hit you for {sandy_damage} damage!")

        if player.health <= 0:
            print(f"\n💔 {player.name} has been defeated by Sandy Cheeks!")
            print("Game Over! Better luck next time!")
            return  # End the game completely
        else:
            print("\n🎉 You defeated Sandy Cheeks!")
            print("You enter the secret formula room, but Mr. Krabs catches you!")
            self.talk_to_mr_krabs()  # Call the dialogue with Mr. Krabs

        print("\n🦀 FINAL BOSS BATTLE: Mr. Krabs 🦀")



    # Call the dialogue with Mr. Krabs

        print("Now it's time to battle Mr. Krabs!")
        player = self.party[0]

        krabs_health = 75
        krabs_base_damage = 10
        krabs_damage_range = 15

        while krabs_health > 0 and player.health > 0:
            print(f"\nMr. Krabs has {krabs_health} health. You have {player.health} health.")
            print("Where would you like to attack Mr. Krabs?")
            print("1. Torso")
            print("2. Arms")
            print("3. Legs")

            attack_choice = input("Enter your choice (1-3): ")

            if attack_choice == "1":
                damage = random.randint(15, 25) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            elif attack_choice in ["2", "3"]:
                damage = random.randint(5, 10) + player.strength.value
                krabs_health -= damage
                print(f"You dealt {damage} damage to Mr. Krabs!")
            else:
                print("Invalid attack choice.")
                continue

            if krabs_health > 0:
                krabs_damage = krabs_base_damage + random.randint(0, krabs_damage_range)
                player.health -= krabs_damage
                print(f"Mr. Krabs hit you for {krabs_damage} damage!")

        if player.health <= 0:
            print(f"\n💔 {player.name} has been defeated by Mr. Krabs!")
            self.display_defeat_dialogue()  # Call the defeat dialogue here
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
        return party[0]

    def select_stat(self, character: Character) -> Statistic:
        return character.strength

    def select_riddle_option(self, options: List[str]) -> str:
        for i, option in enumerate(options, 1):
            print(option)
        return input("Enter the number of your answer (1-3): ")


def main():
    parser = Parser()
    spongebob = Character(name="SpongeBob", health=100, strength=10)

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
    game.start()



if __name__ == "__main__":
    main() 
