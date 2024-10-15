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
        self.health = 160  # werewolves will have the highest base health
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