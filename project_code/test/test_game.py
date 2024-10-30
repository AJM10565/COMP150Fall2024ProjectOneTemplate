import sys
import os

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Statistic, Character, Jedi, BountyHunter, Droid, Event, Location, Game, UserInputParser
import unittest

class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.strength = Statistic("Strength", value=10)

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.value, 10)

    def test_statistic_modify(self):
        self.strength.modify(5)
        self.assertEqual(self.strength.value, 15)
        self.strength.modify(-10)
        self.assertEqual(self.strength.value, 5)

    def test_statistic_min_max_bounds(self):
        self.strength.modify(1000)
        self.assertEqual(self.strength.value, self.strength.max_value)
        self.strength.modify(-1000)
        self.assertEqual(self.strength.value, self.strength.min_value)

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character(name="Leia", strength_value=12, intelligence_value=15)

    def test_character_initialization(self):
        self.assertEqual(self.character.name, "Leia")
        self.assertEqual(self.character.strength.name, "Strength")
        self.assertEqual(self.character.strength.value, 10)
        self.assertEqual(self.character.intelligence.name, "Intelligence")
        self.assertEqual(self.character.intelligence.value, 10)

    def test_character_get_stats(self):
        stats = self.character.get_stats()
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0].name, "Strength")
        self.assertEqual(stats[1].name, "Intelligence")

class TestJedi(unittest.TestCase):

    def setUp(self):
        self.jedi = Jedi(name="Luke")

    def test_jedi_initialization(self):
        self.assertEqual(self.jedi.name, "Luke")
        self.assertEqual(self.jedi.force_sensitivity.name, "Force Sensitivity")
        self.assertEqual(self.jedi.mind_tricks.name, "Mind Tricks")
        self.assertEqual(self.jedi.lightsaber_proficiency.name, "Lightsaber Proficiency")

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event_data = {
            "id": "test_event",
            "passing_attributes": {"Intelligence": "Success message for Intelligence."},
            "partial_pass_attributes": {"Strength": "Partial success message for Strength."},
            "prompt_text": "A locked door blocks your path. How will you proceed?",
            "fail": {"message": "You failed to open the door."},
            "outcomes": {
                "pass": ["next_location_1"],
                "partial_pass": ["next_location_2"],
                "fail": ["next_location_3"]}
        }

        self.event = Event(self.event_data)
        self.character = Character(name="Test Character", strength_value=5, intelligence_value=20)


    def test_event_initialization(self):
        self.assertEqual(self.event.name, "test_event")
        self.assertEqual(self.event.prompt_text, self.event_data["prompt_text"])
        self.assertEqual(self.event.fail_message, self.event_data["fail"]["message"])

    def test_event_execute_pass(self):
        parser = UserInputParser()
        chosen_stat = self.character.intelligence
        event_result = self.event.execute([self.character], parser)
        self.assertIn(event_result, ["pass", "partial_pass", "fail"])

    def test_event_get_next_location(self):
        self.event.status = "pass"
        next_location = self.event.get_next_location()
        self.assertIn(next_location, ["next_location_1", "next_location_2", "next_location_3"])

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.event_data = [
            {"id": "event_1", "passing_attributes": {}, "partial_pass_attributes": {}, "prompt_text": "", "fail": {"message": ""}, "outcomes": {"pass": [], "partial_pass": [], "fail": []}},
            {"id": "event_2", "passing_attributes": {}, "partial_pass_attributes": {}, "prompt_text": "", "fail": {"message": ""}, "outcomes": {"pass": [], "partial_pass": [], "fail": []}}
        ]
        self.events = [Event(data) for data in self.event_data]
        self.location = Location("Test Location", self.events)


    def test_location_get_event(self):
        event = self.location.get_event("event_1")
        self.assertEqual(event.name, "event_1")

        random_event = self.location.get_event(event.name)
        self.assertIn(random_event.name, ["event_1", "event_2"])

class TestGame(unittest.TestCase):

    def setUp(self):
        self.parser = UserInputParser()
        self.characters = [Jedi("Luke"), BountyHunter("Han Solo"), Droid("R2-D2")]
        self.events = [Event({
            "id": "event_1", "passing_attributes": {}, "partial_pass_attributes": {}, "prompt_text": "", "fail": {"message": ""}, "outcomes": {"pass": [], "partial_pass": [], "fail": []}
        })]
        self.locations = [Location("Jedha", self.events), Location("Star Destroyer", self.events)]
        self.game = Game(self.parser, self.characters, self.locations, max_failures=3)

    def test_game_initialization(self):
        self.assertEqual(len(self.game.party), 3)
        self.assertEqual(self.game.current_location.name, "Jedha")
        self.assertEqual(self.game.fail_count, 0)
        self.assertFalse(self.game.is_game_over)

    def test_game_transition_to_star_destroyer(self):
        self.game.transition_to_star_destroyer()
        self.assertEqual(self.game.current_location.name, "Star Destroyer")

    def test_game_end_game_on_max_failures(self):
        self.game.fail_count = 3
        self.game.end_game()
        self.assertTrue(self.game.is_game_over)


if __name__ == '__main__':
    unittest.main()
