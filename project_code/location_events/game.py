import json
import os
import random
from typing import List
from character import Character
from event import Event
from location import Location
from parser import Parser

class SandyCheeks(Character):
    def __init__(self):
        super().__init__(name="Sandy Cheeks", health=120, strength=15)


class Game:
    def __init__(self, parser: Parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.correct_answers = 0
        self.used_riddles = set()

        # Load riddles from JSON file
        # Load riddles from JSON file located in the 'data' directory
        data_path = os.path.join(os.path.dirname(__file__), '..', 'location_events', 'riddles.json')
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