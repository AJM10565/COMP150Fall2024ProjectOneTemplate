# This file will contain the Player class and the progression system logic (XP, leveling up, etc.)
class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 65  # XP needed to reach the next level is 65 (can be changed)

    def gain_xp(self, amount):
        """Increase XP and check for level up."""
        self.xp += amount
        print(f"{self.name} gains {amount} XP. Total XP: {self.xp}/{self.xp_to_next_level}")
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Handle leveling up."""
        self.level += 1
        self.xp -= self.xp_to_next_level  # Subtract the XP needed for the next level
        self.xp_to_next_level += 65  # XP required increases by 65 with each level
        
        # Boost character stats upon leveling up
        self.character.health += 10 * self.level  # Health increases by 10 per level
        self.character.attack += 2 * self.level  # Attack increases by 2 per level
        self.character.defense += 2 * self.level  # Defense increases by 2 per level

        print(f"*** {self.name} has leveled up to Level {self.level}! ***")
        print(f"New Stats -> Health: {self.character.health}, Attack: {self.character.attack}, Defense: {self.character.defense}")

    def show_status(self):
        """Display current player status."""
        print(f"Player: {self.name}")
        print(f"Character: {self.character.name}")
        print(f"Level: {self.level}, XP: {self.xp}/{self.xp_to_next_level}")
        print(f"Health: {self.character.health}, Attack: {self.character.attack}, Defense: {self.character.defense}")
