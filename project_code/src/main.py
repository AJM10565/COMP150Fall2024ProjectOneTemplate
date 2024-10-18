import json
import sys
import random
from typing import List, Optional
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

class Item: # rushi 10/13
    def __init__(self, name: str, item_type: str, effect: str, effect_value: int):
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.effect_value = effect_value

    def describe(self):
        return f"{self.name} ({self.item_type}): {self.effect} by {self.effect_value}!" # gives the item's name, type, and what effect it has

    def use(self, character):
        if self.effect == "increase_glamour":
            character.gain_glamour(self.effect_value)
        elif self.effect == "heal": # how much health the item restores
            character.health.modify(self.effect_value)
            print(f"Bandage! ❤️‍🩹 {character.name} healed for {self.effect_value} health points!")
#Dalila 10/14
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        if item in self.items: # rushi 10/14
            print(f"{item.name} is already in your inventory! No duplicates allowed.")
        else:
            self.items.append(item)
            print (f"{item.name} has been added to your inventory.")
    
    def remove_item(self, item_name: str):
        """Remove an item from the inventory by name."""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                print(f"{item_name} has been removed from your inventory.")
                return
        print(f"{item_name} not found in your inventory!")

    def show_inventory(self):
        if not self.items:
            print("Your inventory is empty! Fill it with some goodies! 💄")
        else:
            print("Inventory contains the following items:")
            for item in self.items:
                print(f"- {item.describe()}")

class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.health = Statistic("Health", 100, description="Tracks remaining health", min_value=0, max_value=100)
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Barbie's sparkling genius!")
        self.glamour_points = 0  #initialize glamour points to zero 
        self.inventory = Inventory() #Dalila 10/14
        self.active_quests = []  # Track ongoing quests
        self.completed_quests = []  # Track completed quests


    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence, self.glamour_points]  # Extend this list if there are more stats
    #dalila 10/11
    def gain_glamour(self, amount: int):
        """Increase Barbies Glamour Points."""
        self.glamour_points += amount
        print(f"{self.name} just had a total glamour boost! They collected {amount} Glamour Points. Total Glamour Points: {self.glamour_points}")

# rushi 10/11
    def take_damage(self, damage: int):
        self.health.modify(-damage)
        print(f"Oh no!💔 {self.name} took {damage} damage. Remaining health: {self.health.value}")
        if self.health.value <= 0:
            print(f"{self.name} has totes been defeated! Time for a relaxing day to recover...")
# rushi 10/11
    def check_stats(self):
        print(f"Stats for {self.name}:")
        print(f"Health: {self.health.value}")
        print(f"Strength: {self.strength.value}")
        print(f"Intelligence: {self.intelligence.value}")
        print(f"Glamour Points: {self.glamour_points}")
# rushi 10/13
    def add_item(self, item: Item):
        self.inventory.add_item(item)
        print(f"{self.name} acquired {item.name}!")
# rushi 10/13
    def use_item(self, item_name: str):
        for item in self.inventory.items:
            if item.name == item_name:
                item.use(self)
                self.inventory.remove_item(item)
                print(f"{self.name} used {item.name}.")
                return
        print(f"{item_name} not found in their purse!")
#dalila 10/14
    def remove_from_inventory(self, item_name: str):
        self.inventory.remove_item(item_name)

    def view_inventory(self):
        self.inventory.show_inventory() # rushi 10/15  
        # rushi 10/15
    def attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.strength.value} damage!")
        target.take_damage(self.strength.value)
    
    def complete_quest(self, quest): # rushi 10/17
        if quest in self.active_quests and not quest.is_completed:
            quest.complete()
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)

            if isinstance(quest.rewards, int):  # Glamour points reward
                self.gain_glamour(quest.rewards)
            elif isinstance(quest.rewards, str):  # Item reward
                self.inventory.add_item(Item(quest.rewards))

    def view_active_quests(self): # rushi 10/17
        """Display active quests."""
        if self.active_quests:
            print("Active Quests:")
            for quest in self.active_quests:
                print(quest)
        else:
            print("No active quests.")

    def view_completed_quests(self): # rushi 10/17
        if self.completed_quests:
            print("Completed Quests:")
            for quest in self.completed_quests:
                print(quest)
        else:
            print("No completed quests.")


#dalila 10/11
class Enemy:
    def __init__(self, name: str, health: int = 100, strength: int = 10, difficulty: str = "easy"):
        self.name = name 
        self.health = Statistic("Health", health, description="Enemy's health", min_value=0, max_value=100)
        self.strength = Statistic("Strength", strength, description="Enemy's Strength")
        self.difficulty = difficulty

    #Dalila 10/16 and rushi 10/16
    def balance_combat(self, player: Character):
        if self.difficulty == 'easy':
            player.strength.modify(10)
            self.strength.modify(-5)
        elif self.difficulty == 'hard':
            self.strength.modify(5)
            player.strength.modify(-5)

    def __str__(self):
        return f"Enemy: {self.name}, Health: {self.health}, Strength: {self.strength}"
    
    def take_damage(self, damage: int):
        self.health.modify(-damage)
        if self.health.value <= 0:
            print(f"{self.name} has been defeated!")
    
    def attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.strength.value} damage!")
        target.take_damage(self.strength.value)

    def basic_combat_test(): # rushi 10/14
        print("Starting the fabulous face-off! \n")

        barbie = Character(name="Barbie")
        glamazon = Enemy(name="Glamazon", health=80, strength=15)

        print(barbie)
        print(glamazon)

        print("\n--- Round 1: Enemy takes the first move! 💥 ---")
        glamazon.attack(barbie)
        barbie.check_stats()

        print("\n--- Round 2: Barbie uses her glamour attack! ---")
        barbie.gain_glamour(20) 
        glamazon.take_damage(20)
        print(glamazon)

        if glamazon.health.value > 0:
            print("\n--- Round 3: Enemy fights back! ⚔️ ---")
            glamazon.attack(barbie)

        print("\n--- Final Stats: Who wore the crown best? 👑 ---")
        barbie.check_stats()
        print(glamazon)

    basic_combat_test()


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

        # rushi 10/18
        self.npcs = [
            NPC(name="Midge", dialogue="Hello, darling! Ready for a new adventure? 👭", quests=[], store_items=[]),
            NPC(name="Mermaid", dialogue="Welcome to my underwater kingdom! 🧜‍♀️ Care to explore?", quests=[], store_items=[]),
            NPC(name="Fairy Godmother", dialogue="I have some magical items for you! 🪄", quests=[], store_items=[]),
        ]

        self.continue_playing = True

    def interact_with_npc(self): # rushi 10/18
        print("Who would you like to talk to?")
        for idx, npc in enumerate(self.npcs):
            print(f"{idx + 1}. {npc.name}")

        choice = int(input("Enter the number of the NPC to talk to: ")) - 1
        if 0 <= choice < len(self.npcs):
            npc = self.npcs[choice]
            npc.talk()

        print("What would you like to do?")
        print("1. Accept a quest")
        print("2. Buy an item")
        print("3. Leave")

        action = input("Enter your choice: ")

        if action == "1":
            quest = npc.offer_quest()
            if quest:
                self.party[0].active_quests.append(quest)  # Assign quest to player
        elif action == "2":
            npc.sell_items(self.party[0])
        elif action == "3":
            print("You left the conversation.")
        else:
            print("Not quite right!")

    
    #dalila 10/15
    def battle(self, player: Character, enemy: Enemy):
        print(f"{player.name} has encountered {enemy.name}!")

        while player.health.value > 0 and enemy.health.value > 0: 
            print(" /nWhat will you do? ")
            print("1. Attack")
            print("2. Use Item")
            print("3. Run")
            
            choice = input("Enter your choice: ")

            if choice == "1":
               print(f"{player.name} attacks {enemy.name}!")
               player.attack(enemy)
               if  enemy.health.value <= 0:
                   print(f"{enemy.name} has been defeated 🎉")
                   break
            
            elif choice == "2":
                player.view_inventory() # rushi 10/16
                item_name = input("Enter the name of the item to use: ")
                player.use_item(item_name)

            elif choice == "3":
                if random.random() > 0.5:
                    print(f"{player.name} successfully ran away 🏃‍♀️")
                    break 
                else:
                    print(f"{player.name} failed to run away! ")
            
            if enemy.health.value > 0:
                print(f"{enemy.name} strikes back!")
                enemy.attack(player)

            if player.health.value <= 0:
                print(f"{player.name} has been defeated! 💔 Game Over.")


    def get_valid_input(self, prompt: str, valid_choices: List[int]) -> int: #rushi 10/12
        while True:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"Pretty please, enter a valid choice: {valid_choices}")
            except ValueError:
                print("Not quite right! Please enter a number. ♡ ")

    def start(self):
        items = [ # rushi 10/13
            Item(name="Glitter Heels", item_type="Accessory", effect="increase_glamour", effect_value=10),
            Item(name="Magic Wand", item_type="Weapon", effect="increase_intelligence", effect_value=15),
            Item(name="Glamourous Tiara", item_type="Accessory", effect="increase_glamour", effect_value=15),
            Item(name="Beauty Potion", item_type="Consumable", effect="heal", effect_value=30),
            Item(name="Fabulous Sunglasses", item_type="Accessory", effect="increase_charm", effect_value=7),
            Item(name="Dreamy Backpack", item_type="Accessory", effect="increase_inventory_space", effect_value=3),
            Item(name="Powerful Perfume", item_type="Consumable", effect="increase_glamour", effect_value=12),
            Item(name="Fashion Magazine", item_type="Item", effect="increase_intelligence", effect_value=8),
        ]

        for item in items:
            self.party[0].add_item(item)
        # rushi 10/11
        while self.continue_playing:
            print("🎉 Welcome to Barbie's Adventure! 🎉")
            print("What would you like to do?")
            print("1. Check Player Stats")
            print("2. Gain Glamour Points ✨")
            print("3. Simulate a Fight")
            print("4. Exit Game 😔")
            print("5. Manage Inventory 👜")            
            
            choice = self.get_valid_input("Enter your number!: ", [1, 2, 3, 4])

            if choice == 1:
                for character in self.party:
                    character.check_stats()

            elif choice == 2:
                amount = int(input("Enter the amount of glamour points to gain: "))
                for character in self.party:
                    character.gain_glamour(amount)
            # rushi 10/15
            elif choice == 3:
                self.start_combat()
                
            elif choice == 4:
                # Exit game
                print("Thanks for playing! 💖 See you next time!")
                self.continue_playing = False

            elif choice == 5: # rushi 10/18
                self.manage_inventory()

            else:
                print("That's not quite right. Please try again.")
        print("Game Over.")

    def manage_inventory(self):
        player = self.party[0]
        while True:
            print("\nInventory Management:")
            player.view_inventory()

            print("1. Use an item")
            print("2. Remove an item")
            print("3. Exit Inventory Management")

            choice = self.get_valid_input("Enter your choice: ", [1, 2, 3])

            if choice == 1:
                item_name = input("Enter the name of the item to use: ")
                player.use_item(item_name)

            elif choice == 2:
                item_name = input("Enter the name of the item to remove: ")
                player.remove_from_inventory(item_name)

            elif choice == 3:
                print("Exiting inventory management.")
                break

    def start_combat(self): # rushi 10/15
        enemies = [
            Enemy(name="Glamazon", health=80, strength=15),
            Enemy(name="Fashion Police", health=60, strength=10),
            Enemy(name="Mean Girl", health=70, strength=12),
            Enemy(name="Bad Hair Day", health=50, strength=8)
        ]

        print("An enemy approaches! 🌟")
        chosen_enemy = self.parser.select_enemy(enemies)
        print(f"You chose to fight {chosen_enemy.name}! 💥")

        self.battle(self.party[0], chosen_enemy)

        for character in self.party:
            print(f"{character.name} attacks {chosen_enemy.name}!")
            character.attack(chosen_enemy)
            if chosen_enemy.health.value <= 0:
                print(f"Victory! {chosen_enemy.name} has been defeated! 🎉")
                return 

            print(f"{chosen_enemy.name} fights back!")
            chosen_enemy.attack(character)

            if character.health.value <= 0:
                print(f"{character.name} lost all their sparkle! 🚫")
                return

        print("The fight is over. Rest up, warrior!")
    def check_game_over(self):
        return len(self.party) == 0

class Quest: # rushi 10/17
    def __init__(self, name, description, rewards):
        self.name = name
        self.description = description
        self.rewards = rewards
        self.is_completed = False

    def complete(self):
        self.is_completed = True
        print(f"Quest '{self.name}' completed! ✩ You earned: {self.rewards}")

    def __str__(self):
        return f"Quest: {self.name}\nDescription: {self.description}\nReward: {self.rewards}"

class NPC: # rushi 10/18
    def __init__(self, name: str, dialogue: str, quests: List[Quest] = None, store_items: List[Item] = None):
        self.name = name
        self.dialogue = dialogue
        self.quests = quests or []
        self.store_items = store_items or []

    def interact(self, player: Character):
        print(f"{self.name}: {self.dialogue}")
        print("1. Accept Quest")
        print("2. Buy Items 🛒")
        print("3. Leave")
        
        choice = input("What would you like to do? ")

        if choice == "1":
            self.offer_quest(player)
        elif choice == "2":
            self.sell_items(player)
        else:
            print(f"{self.name}: Come back anytime, darling! 👋")

    def offer_quest(self, player: Character):
        if self.quests:
            print("Available Quests:")
            for idx, quest in enumerate(self.quests):
                print(f"{idx + 1}. {quest.name}: {quest.description}")
            choice = int(input("Enter the number of the quest to accept: ")) - 1
            selected_quest = self.quests.pop(choice)
            player.active_quests.append(selected_quest)
            print(f"{player.name} accepted the quest: {selected_quest.name}")
        else:
            print(f"{self.name}: Sorry, no quests available right now. 🤷‍♀️")

    def sell_items(self, player: Character):
        if self.store_items:
            print("Items for Sale:")
            for idx, item in enumerate(self.store_items):
                print(f"{idx + 1}. {item.describe()}")
            choice = int(input("Enter the number of the item to buy: ")) - 1
            selected_item = self.store_items.pop(choice)
            player.add_item(selected_item)
            print(f"{player.name} bought {selected_item.name}.")
        else:
            print(f"{self.name}: Sorry, I'm all out of stock. 😔")


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
    # rushi 10/15
    def select_enemy(self, enemies: List[Enemy]) -> Enemy:
        print("Choose an enemy to fight:")
        for idx, enemy in enumerate(enemies):
            print(f"{idx + 1}. {enemy.name} (Health: {enemy.health.value}, Strength: {enemy.strength.value})")
        choice = int(self.parse("Enter the number of the enemy: ")) - 1
        return enemies[choice]


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
