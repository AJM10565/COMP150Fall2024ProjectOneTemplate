
from character import Character  # Relative import from the same directory
import random  # Import Python's random module


class Vampire(Character):
    def __init__(self, name, level=1):
        # Initialize the base Character with name, level, and initial health
        super().__init__(name, level, health=120, attack=10, defense=9)
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
            super().take_damage(amount)  # Call the base class method to handle health reduction
            print(f"{self.name} takes {amount} damage. Health is now {self.health}.")

    def heal(self, amount):
        """Restore health when Life Drain is used."""
        self.health = min(self.max_health, self.health + amount)  # Ensure health doesn't exceed max_health
        print(f"{self.name} heals for {amount}. Health is now {self.health}.")
