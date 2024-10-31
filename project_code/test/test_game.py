import unittest
import io
from unittest.mock import patch
import sys
import os

from project_code.src.main import Character, Jedi, BountyHunter, Droid, Event, UserInputParser, Statistic, EventStatus

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



class TestCharacter(unittest.TestCase):

    def test_character_initialization(self):
        character = Character("Test Character")
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(len(character.stats), 2)

    def test_jedi_stats(self):
        jedi = Jedi("Luke")
        self.assertEqual(jedi.name, "Luke")
        self.assertEqual(len(jedi.stats), 5)  # Jedi should have 5 stats

    def test_bounty_hunter_stats(self):
        hunter = BountyHunter("Han Solo")
        self.assertEqual(hunter.name, "Han Solo")
        self.assertEqual(len(hunter.stats), 5)  # BountyHunter should have 5 stats

    def test_droid_stats(self):
        droid = Droid("R2-D2")
        self.assertEqual(droid.name, "R2-D2")
        self.assertEqual(len(droid.stats), 4)  # Droid should have 4 stats


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event_data = {
            "id": "test_event",
            "passing_attributes": {"Strength": "You passed with strength."},
            "partial_pass_attributes": {"Intelligence": "You partially passed with intelligence."},
            "prompt_text": "A test event prompt.",
            "fail": {"message": "You failed the event."},
            "outcomes": {
                "pass": ["next_event_1"],
                "partial_pass": ["next_event_2"],
                "fail": ["next_event_3"]
            }
        }
        self.event = Event(self.event_data)



    @patch('project_code.src.main.UserInputParser.select_party_member')
    @patch('project_code.src.main.UserInputParser.select_stat')
    def test_event_execution_pass(self, mock_select_stat, mock_select_party_member):
        character = Character("Test Character")
        stat = character.stats[0]  # Assume 'Strength' is chosen for simplicity
        mock_select_party_member.return_value = character
        mock_select_stat.return_value = stat

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            parser = UserInputParser()
            outcome = self.event.execute([character], parser)
            self.assertEqual(outcome, "pass")
            self.assertIn("You passed with strength.\n", mock_stdout.getvalue())


    def test_resolve_choice(self):
        character = Character("Test Character")
        self.assertEqual(self.event.resolve_choice(character, character.stats[0]), EventStatus.PASS)


class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.strength = Statistic("Strength", description="Strength measures physical power.")

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.description, "Strength measures physical power.")

    def test_statistic_str_method(self):
        self.assertEqual(str(self.strength), "Strength")


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


if __name__ == '__main__':
    unittest.main()
