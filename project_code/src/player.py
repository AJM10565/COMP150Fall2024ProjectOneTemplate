from src.witch import Witch
from src.vampire import Vampire
from src.werewolf import Werewolf
from project_code.src import Character

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

# creating tests to verify that a player can gain points without leveling up
import unittest

class PlayerTest(unittest.TestCase):
    
    def setUp(self):
        """Set up unit test with a player and a character."""
        self.character = Character("Test Vampire", 100, 15, 10)
        self.player = Player("Klaus", self.character)
    
    def test_gain_xp_no_level_up(self):
        """Test gaining points without leveling up."""
        self.player.gain_xp(30)
        self.assertEqual(self.player.xp, 30)
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.character.health, 100)

    def test_gain_xp_and_level_up(self):
        """Test gaining enough points to level up."""
        self.player.gain_xp(65)
        self.assertEqual(self.player.level, 2)  # should level up
        self.assertEqual(self.player.xp, 0)  # points reset after level up
        self.assertEqual(self.player.xp_to_next_level, 130)  # points required increases
        self.assertEqual(self.player.character.health, 120)  # health increases
        self.assertEqual(self.player.character.attack, 19)   # attack increases
        self.assertEqual(self.player.character.defense, 14)  # defense increases
if __name__ == '__main__':
    unittest.main()
