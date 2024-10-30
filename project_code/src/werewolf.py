from character import Character  # Relative import from the same directory
import random  # Import Python's random module

class Werewolf(Character):
    def __init__(self, name, level=1):
        # Initialize the base Character with name, level, and initial health
        super().__init__(name, level, health=145, attack=12, defense=8)
        self.bloodlust_active = False  # Special trait flag
        self.bloodlust_attack_boost = 0  # Extra stacks from the Bloodlust trait

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
        damage = self.attack * 1.5  # This attack is stronger than the basic attack

        if random.random() <= critical_hit_chance:
            damage *= 2  # A critical hit will hit for double the damage
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
        super().take_damage(amount)  # Call the base class method to manage health
        print(f"{self.name} takes {amount} damage. Health is now {self.health}.")
