# Add the root directory of the project to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Statistic, Character, Jedi, BountyHunter, Droid, Event, EventStatus, display_opening_crawl, display_star_destroyer_prompt, display_winning_crawl
from project_code.src.opening_crawl import display_opening_crawl
from project_code.src.star_destroyer_prompt import display_star_destroyer_prompt
from project_code.src.display_winning_crawl import display_winning_crawl

import unittest

class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.strength = Statistic("Strength", description="Strength measures physical power.")

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.description, "Strength measures physical power.")

    def test_statistic_str_method(self):
        self.assertEqual(str(self.strength), "Strength")


class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character(name="Hero")

    def test_character_initialization(self):
        self.assertEqual(self.character.name, "Hero")
        self.assertEqual(self.character.stats[0].name, "Strength")
        self.assertEqual(self.character.stats[1].name, "Intelligence")

    def test_character_stats_names(self):
        stats_names = [str(stat) for stat in self.character.stats]
        self.assertIn("Strength", stats_names)
        self.assertIn("Intelligence", stats_names)


class TestJedi(unittest.TestCase):

    def setUp(self):
        self.jedi = Jedi(name="Luke")

    def test_jedi_initialization(self):
        self.assertEqual(self.jedi.name, "Luke")
        self.assertEqual(self.jedi.stats[2].name, "Force Sensitivity")
        self.assertEqual(self.jedi.stats[3].name, "Mind Tricks")
        self.assertEqual(self.jedi.stats[4].name, "Lightsaber Proficiency")


class TestBountyHunter(unittest.TestCase):

    def setUp(self):
        self.bounty_hunter = BountyHunter(name="Han Solo")

    def test_bounty_hunter_initialization(self):
        self.assertEqual(self.bounty_hunter.name, "Han Solo")
        self.assertEqual(self.bounty_hunter.stats[2].name, "Dexterity")
        self.assertEqual(self.bounty_hunter.stats[3].name, "Blaster Proficiency")
        self.assertEqual(self.bounty_hunter.stats[4].name, "Piloting")


class TestDroid(unittest.TestCase):

    def setUp(self):
        self.droid = Droid(name="R2-D2")

    def test_droid_initialization(self):
        self.assertEqual(self.droid.name, "R2-D2")
        self.assertEqual(self.droid.stats[2].name, "Processing")
        self.assertEqual(self.droid.stats[3].name, "Hacking")


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event_data = {
            "id": "test_event",
            "passing_attributes": {"Intelligence": "You solved the puzzle."},
            "partial_pass_attributes": {"Strength": "You forced the door open halfway."},
            "prompt_text": "A door blocks your path, covered in puzzles.",
            "fail": {"message": "You couldn't open the door."},
            "outcomes": {"pass": ["next_event"], "partial_pass": ["another_event"], "fail": ["retry_event"]}
        }
        self.event = Event(self.event_data)

    def test_event_initialization(self):
        self.assertEqual(self.event.name, "test_event")
        self.assertEqual(self.event.prompt_text, "A door blocks your path, covered in puzzles.")
        self.assertEqual(self.event.fail_message, "You couldn't open the door.")
        self.assertEqual(self.event.outcomes["pass"], ["next_event"])

    def test_event_resolve_choice_pass(self):
        mock_character = Character()
        mock_character.stats[1].name = "Intelligence"  # Set stat to match pass condition
        self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[1]), EventStatus.PASS)

    def test_event_resolve_choice_partial_pass(self):
        mock_character = Character()
        mock_character.stats[0].name = "Strength"  # Set stat to match partial pass condition
        self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[0]), EventStatus.PARTIAL_PASS)

    def test_event_resolve_choice_fail(self):
        mock_character = Character()
        mock_character.stats[0].name = "Dexterity"  # Set stat to trigger fail condition
        self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[0]), EventStatus.FAIL)


if __name__ == '__main__':
    unittest.main()
