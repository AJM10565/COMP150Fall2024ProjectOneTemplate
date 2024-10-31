import unittest
from unittest.mock import patch, MagicMock
from ..src.main import start_game, Game, UserInputParser, Location, EventStatus

from src.witch import Witch
from src.werewolf import Werewolf
from src.vampire import Vampire
from src.event import GameEvent
from src.character import Character


class TestGame(unittest.TestCase):

    def setUp(self):
        """Set up a test game environment before each test."""
        self.parser = UserInputParser()
        self.witch = Witch("Test Witch")
        self.werewolf = Werewolf("Test Werewolf")
        self.vampire = Vampire("Test Vampire")
        
        # Create a sample event for testing
        self.event_data = {
            'primary_attribute': 'Strength',
            'secondary_attribute': 'Intelligence',
            'prompt_text': 'You encounter a challenge.',
            'pass': {'message': 'You passed!'},
            'fail': {'message': 'You failed!'},
            'partial_pass': {'message': 'Partial success.'}
        }
        self.event = GameEvent(self.event_data)
        self.location = Location([self.event])
        self.game = Game(self.parser, [self.witch, self.werewolf, self.vampire], [self.location])

    def test_character_initialization(self):
        """Test that characters are initialized correctly."""
        self.assertEqual(self.witch.health, 100)
        self.assertEqual(self.werewolf.health, 100)
        self.assertEqual(self.vampire.health, 120)

    def test_perform_quest(self):
        """Test that the quest performs correctly."""
        self.game.perform_quest()  # This will invoke the event
        self.assertIn(self.event.status, [EventStatus.PASS, EventStatus.PARTIAL_PASS, EventStatus.FAIL])

    def test_check_game_over(self):
        """Test game over logic when all characters are dead."""
        self.witch.take_damage(100)  # Simulate damage
        self.werewolf.take_damage(100)
        self.vampire.take_damage(120)
        self.assertTrue(self.game.check_game_over())

    @patch('builtins.input', side_effect=['1'])  # Mock input to select the first character
    def test_start_game(self, mock_input):
        """Test starting the game with character selection."""
        with patch('src.main.print') as mock_print:
            start_game()
            mock_print.assert_any_call("Choose your character:")
            mock_print.assert_any_call("1. Witch")
            mock_print.assert_any_call("You encounter a challenge.")

if __name__ == '__main__':
    unittest.main()
