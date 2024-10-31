import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure `src` directory inside `project_code` is added to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
path = os.path.abspath('src')
sys.path.append(path)
import main.py

from .subdir import Game, UserInputParser, Location, EventStatus
from character import Character
from event import GameEvent


class TestGame(unittest.TestCase):

    def setUp(self):
        # Mock parser to simulate user input
        self.parser = MagicMock()
        # Sample characters for testing
        self.character1 = Character("Witch", health=100)
        self.character2 = Character("Werewolf", health=100)
        self.party = [self.character1, self.character2]
        
        # Sample events
        event_data_1 = {
            "prompt_text": "A goblin appears!",
            "outcomes": {"win": {"message": "You defeated the goblin!", "health_change": 0}}
        }
        event_data_2 = {
            "prompt_text": "You encounter a riddle.",
            "options": {
                "solve": {"success": {"message": "You solved the riddle!", "health_change": 0}},
                "fail": {"message": "You failed the riddle.", "health_change": -10}
            }
        }
        self.events = [GameEvent(event_data_1), GameEvent(event_data_2)]
        self.locations = [Location(self.events)]
        
        # Instantiate game instance
        self.game = Game(self.parser, self.party, self.locations)

    def test_start_game(self):
        # Simulate `parser.parse` to control user choices
        self.parser.parse.side_effect = ["1", "2", "1", "1", "2", "1", "2"]
        with patch("builtins.print") as mocked_print:
            self.game.start()
            # Ensure the final choice prompt is shown in the last quest
            mocked_print.assert_any_call("You find a glowing ruby resting on a stone pedestal in the woods. Do you destroy it or take it?")

    def test_final_choice_destroy_ruby(self):
        # Simulate choice for "destroy ruby" in the final quest
        self.parser.parse.return_value = "1"
        with patch("builtins.print") as mocked_print:
            self.game.final_choice()
            # Check for correct final message
            mocked_print.assert_any_call("You see the fog clearing up! You have saved Halloween Night. Congratulations!")
            self.assertFalse(self.game.continue_playing)

    def test_final_choice_take_ruby(self):
        # Simulate choice for "take ruby" in the final quest
        self.parser.parse.return_value = "2"
        with patch("builtins.print") as mocked_print:
            self.game.final_choice()
            # Check for the warning message and the loop reset
            mocked_print.assert_any_call("The ruby sears your hand and a powerful beast summons and knocks you out cold! Greed is never the answer...")
            self.assertEqual(self.game.current_quest, 0)

    def test_trigger_random_event_fight_win(self):
        # Test a win in a random fight event
        self.parser.parse.return_value = "1"  # Choose to attack directly
        with patch("builtins.print") as mocked_print:
            with patch("random.choice", side_effect=["fight", "win"]):
                self.game.trigger_random_event()
                mocked_print.assert_any_call("You bravely fought and defeated the enemy! You continue your journey.")

    def test_trigger_random_event_obstacle_hurt(self):
        # Test getting hurt in an obstacle event
        self.parser.parse.return_value = "1"  # Choose option to bypass obstacle
        with patch("builtins.print") as mocked_print:
            with patch("random.choice", side_effect=["obstacle", "hurt"]):
                self.game.trigger_random_event()
                mocked_print.assert_any_call("You got hurt trying to bypass the obstacle.")
                self.assertLess(self.character1.health, 100)
                self.assertLess(self.character2.health, 100)

    def test_check_game_over(self):
        # Set all characters' health to 0 to simulate game over
        self.character1.health = 0
        self.character2.health = 0
        self.assertTrue(self.game.check_game_over())

    def test_heal_party_member_in_mystery_event(self):
        # Test finding a health potion in a mystery event
        self.character1.health = 50  # Lower health to see the heal effect
        self.parser.parse.return_value = "1"  # Choose option to search
        with patch("builtins.print") as mocked_print:
            with patch("random.choice", side_effect=["mystery", "health_potion"]):
                self.game.trigger_random_event()
                mocked_print.assert_any_call("You found a health potion!")
                self.assertGreater(self.character1.health, 50)  # Verify healing occurred


if __name__ == "__main__":
    unittest.main()
