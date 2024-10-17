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

# vampire
class Vampire(Character):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.health = 120  # vampires have moderate health
        self.attack = 10
        self.defense = 9
        self.dodge_chance = 0.2  # SPECIAL TRAIT (Vampiric Reflexes): 20% chance to dodge attacks

    def basic_attack(self, enemy):
        """Perform a basic attack."""
        damage = self.attack - enemy.defense
        if damage > 0:
            enemy.take_damage(damage)
            print(f"{self.name} strikes {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack couldn't break through {enemy.name}'s defense!")

    def life_drain(self, enemy):
        """Perform a special attack that drains health from the enemy while also healing themselves."""
        drain_percentage = 0.3  # 30% of the damage is converted into healing
        damage = self.attack * 1.3  # Life Drain is slightly stronger than a basic attack
        
        damage -= enemy.defense
        if damage > 0:
            enemy.take_damage(damage)
            healing = int(damage * drain_percentage)  # Heal the vampire by a percentage of damage dealt
            self.heal(healing)
            print(f"{self.name} uses Life Drain on {enemy.name}, dealing {damage} damage and restoring {healing} health!")
        else:
            print(f"{self.name}'s Life Drain couldn't break through {enemy.name}'s defense!")

    def vampiric_reflexes(self):
        """Special trait: Vampiric Reflexes give the vampire a chance to dodge attacks."""
        dodge_success = random.random() < self.dodge_chance  # 20% chance to dodge
        return dodge_success

    def take_damage(self, amount):
        """Handle taking damage with a chance to dodge the attack."""
        if self.vampiric_reflexes():
            print(f"{self.name} dodges the attack with Vampiric Reflexes!")
        else:
            super().take_damage(amount)
            print(f"{self.name} takes {amount} damage. Health is now {self.health}.")

    def heal(self, amount):
        """Restore health when Life Drain is used."""
        self.health += amount
        print(f"{self.name} heals for {amount}. Health is now {self.health}.")

# werewolf class
class Werewolf(Character):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.health = 145  # werewolves will have the highest base health
        self.attack = 12
        self.defense = 8
        self.bloodlust_active = False  # Special trait flag
        self.bloodlust_attack_boost = 0  # this will store the extra stacks from the bloodlust trait

    def basic_attack(self, enemy):
        """Perform a basic attack."""
        damage = self.attack - enemy.defense
        if damage > 0:
            enemy.take_damage(damage)
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack couldn't break through {enemy.name}'s defense!")

    def feral_swipe(self, enemy):
        """Perform a special offensive attack with a chance for a critical hit."""
        critical_hit_chance = 0.2  # 20% chance to land a critical hit
        damage = self.attack * 1.5  # this attack is stronger than the basic attack

        if random.random() <= critical_hit_chance:
            damage *= 2  # a critical hit will hit for double the damage
            print(f"A CRITICAL HIT!!! {self.name} swipes ferociously!")
        
        damage -= enemy.defense
        if damage > 0:
            enemy.take_damage(damage)
            print(f"{self.name} uses Feral Swipe on {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name}'s Feral Swipe couldn't break through {enemy.name}'s defense!")

    def bloodlust(self):
        """Activate Bloodlust, which boosts the Werewolf's attack after defeating an enemy."""
        self.bloodlust_active = True
        self.bloodlust_attack_boost += 5  # Each kill increases attack by 5
        print(f"{self.name} has entered a state of Bloodlust! Attack increased by {self.bloodlust_attack_boost}.")

    def attack_enemy(self, enemy):
        """Overrides attack_enemy to handle Bloodlust bonuses."""
        damage = (self.attack + self.bloodlust_attack_boost) - enemy.defense
        if damage > 0:
            enemy.take_damage(damage)
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack couldn't break through {enemy.name}'s defense!")

        # If the enemy is defeated, trigger Bloodlust
        if not enemy.is_alive():
            self.bloodlust()

    def take_damage(self, amount):
        """Handle taking damage, reducing health accordingly."""
        super().take_damage(amount)
        print(f"{self.name} takes {amount} damage. Health is now {self.health}.")

# witch
class Witch(Character):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.health = 100
        self.attack = 11
        self.defense = 6
        self.mana = 0  # mana (her source of magic) starts at 0 and charges up
        self.max_mana = 60  # max mana required to trigger Power Surge(special trait where attacks are more pwerful for 3 turns)
        self.power_surge_active = False  # whether Power Surge is active
        self.power_surge_turns = 0  # number of turns Power Surge is active
        self.power_surge_attack_boost = 10  # attack boost during Power Surge

    def basic_attack(self, enemy):
        """Perform a basic magical attack and charge 6 mana."""
        damage = self.attack - enemy.defense
        if self.power_surge_active:
            damage += self.power_surge_attack_boost  # Boost attack during Power Surge
        
        if damage > 0:
            enemy.take_damage(damage)
            print(f"{self.name} casts Hex Bolt, dealing {damage} damage to {enemy.name}!")
        else:
            print(f"{self.name}'s Hex Bolt couldn't break through {enemy.name}'s defenses!")

        self.charge_mana(6)  # Gain 6 mana with each basic attack

    def curse_of_weakness(self, enemy): # special attack
        """Perform a special attack that reduces the enemy's attack and defense, and charge 12 mana."""
        debuff_amount = 3  # Reduces both attack and defense by 3
        enemy.attack -= debuff_amount
        enemy.defense -= debuff_amount
        print(f"{self.name} casts Curse of Weakness on {enemy.name}, reducing their attack and defense by {debuff_amount} for 3 turns!")

        self.charge_mana(12)  # Gain 12 mana with each special attack

    def charge_mana(self, amount):
        """Charge mana from attacks and activate Power Surge if mana is full."""
        self.mana += amount
        if self.mana >= self.max_mana and not self.power_surge_active:
            self.activate_power_surge()
        print(f"{self.name} charges {amount} mana. Mana is now {self.mana}/{self.max_mana}.")

    def activate_power_surge(self):
        """Activate Power Surge, boosting attacks for 3 rounds."""
        self.power_surge_active = True
        self.power_surge_turns = 3  # Power Surge lasts for 3 turns
        self.mana = 0  # Reset mana after activation
        print(f"{self.name} enters a Power Surge! Attacks are greatly enhanced for the next 3 rounds!")

    def end_turn(self):
        """Manage the duration of Power Surge."""
        if self.power_surge_active:
            self.power_surge_turns -= 1
            if self.power_surge_turns <= 0:
                self.power_surge_active = False
                print(f"{self.name}'s Power Surge has ended.")
    
    def take_damage(self, amount):
        """Handle taking damage."""
        self.health -= amount
        print(f"{self.name} takes {amount} damage. Health is now {self.health}.")

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