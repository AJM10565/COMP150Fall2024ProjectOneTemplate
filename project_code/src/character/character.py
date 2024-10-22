import random
# base character class
class Character:
    def __init__(self, name, level=1, health=100, attack=10, defense=5):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        damage = self.attack - enemy.defense
        if damage > 0:
            enemy.take_damage(damage)


# setting up the random events
import random

class Event:
    def __init__(self, description, event_type):
        self.description = description
        self.event_type = event_type  # 'battle', 'item', 'recruit', 'run'

def trigger_event(character):
    # Define the possible event types
    event_types = ['battle', 'find_item', 'recruit_member', 'run']
    
    # Randomly select an event
    event = random.choice(event_types)
    print(f"Event triggered: {event.replace('_', ' ').capitalize()}")
    
    # Define a possible enemy for battle events
    enemy = Character("Angry Monster", level=2)  ### Just a placeholder for now 
    
    # Trigger a corresponding event based on the random selection
    if event == 'battle':
        handle_battle_event(character, enemy)
    elif event == 'find_item':
        handle_item_event(character)
    elif event == 'recruit_member':
        handle_recruit_event(character)
    elif event == 'run':
        handle_run_event(character, enemy)
    else:
        print("Unknown event type.")

# Example for the battle event handler
def handle_battle_event(character, enemy):
    print(f"A battle begins between {character.name} and {enemy.name}!")
    while character.is_alive() and enemy.is_alive():
        character.attack_enemy(enemy)  # player attacks first
        if enemy.is_alive():
            enemy.attack_enemy(character)  # enemy attacks back
    if character.is_alive():
        print(f"{character.name} has defeated {enemy.name}!")
    else:
        print(f"{character.name} has been defeated by {enemy.name}!")

# Example for the item event handler
def handle_item_event(character):
    item_found = "health potion"
    print(f"{character.name} found a {item_found}!")
    character.heal(20)  # heal player by 20 health (for this example)
    print(f"{character.name} heals for 20 health. Current health: {character.health}.")

# Example for the recruit event handler
def handle_recruit_event(character):
    new_member = Character("Friendly Creature", level=1)  # Again, just a placeholder
    print(f"{character.name} encountered a friendly creature and can recruit {new_member.name}!")
    ### Logic for recruitment will go here *come back to this*

# Example for the run event handler
def handle_run_event(character, enemy):
    print(f"{character.name} tries to run from {enemy.name}.")
    run_success = random.choice([True, False])  # 50% chance to run away
    if run_success:
        print(f"{character.name} successfully escaped!")
    else:
        print(f"{character.name} failed to escape and must fight!")
        handle_battle_event(character, enemy)  # trigger battle if escape plan fails

# testing them to verify / example usage
player_character = Character("Hero", level=1)
trigger_event(player_character)