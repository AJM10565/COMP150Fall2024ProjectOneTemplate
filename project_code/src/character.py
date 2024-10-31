import random
# base character class
class Character:
    def __init__(self, name, level=1, health=100, attack=10, defense=5):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = health  # Initialize max_health to the initial health
        self.attack = attack
        self.defense = defense

    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)  # Use max_health to limit healing
        print(f"{self.name} healed for {amount} points. Current health: {self.health}")

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
            print(f"{self.name} attacked {enemy.name} for {damage} damage.")
        else:
            print(f"{self.name}'s attack was too weak to harm {enemy.name}.")