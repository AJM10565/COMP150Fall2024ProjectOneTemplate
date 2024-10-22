from .character import Character  # Relative import from the same directory
# vampire.py
import random  # Import Python's random module
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