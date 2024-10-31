import unittest
from unittest.mock import patch
from project_code.src.main import (
    Character, Jedi, BountyHunter, Droid, Event, Location, Game, UserInputParser, EventStatus, load_events_from_json
)

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

    @patch('project_code.UserInputParser.select_party_member')
    @patch('project_code.UserInputParser.select_stat')
    def test_event_execution_pass(self, mock_select_stat, mock_select_party_member):
        # Mock a character and selected stat for testing
        character = Character("Test Character")
        stat = character.stats[0]  # Assume 'Strength' is chosen for simplicity

        mock_select_party_member.return_value = character
        mock_select_stat.return_value = stat

        # Execute the event and check if the correct message is displayed for passing
        with patch('sys.stdout') as mock_stdout:
            outcome = self.event.execute([character], UserInputParser())
            self.assertEqual(outcome, "pass")
            mock_stdout.write.assert_called_with("You passed with strength.\n")

    def test_resolve_choice(self):
        character = Character("Test Character")
        self.assertEqual(self.event.resolve_choice(character, character.stats[0]), EventStatus.PASS)


class TestGame(unittest.TestCase):

    from project_code.src.display_winning_crawl import display_winning_crawl
    from project_code.src.star_destroyer_prompt import display_star_destroyer_prompt

    def display_winning_crawl():
        print("You have won the game!")

    def display_star_destroyer_prompt():
        print("Welcome to the Star Destroyer!")


    def setUp(self):
        # Create mock data and instances for the Game class
        self.parser = UserInputParser()
        self.characters = [Jedi("Luke"), Droid("R2-D2")]
        jedha_events = load_events_from_json('project_code/location_events/jedha_events.json')
        star_destroyer_events = load_events_from_json('project_code/location_events/star_destroyer_events.json')
        
        self.locations = [
            Location("Jedha", jedha_events),
            Location("Star Destroyer", star_destroyer_events)
        ]
        self.game = Game(self.parser, self.characters, self.locations, max_failures=5)

    def test_game_initialization(self):
        self.assertEqual(self.game.fail_count, 0)
        self.assertFalse(self.game.is_game_over)

    @patch('project_code.UserInputParser.select_party_member')
    @patch('project_code.UserInputParser.select_stat')
    def test_event_execution_in_game(self, mock_select_stat, mock_select_party_member):
        # Setup mocks
        mock_select_party_member.return_value = self.characters[0]
        mock_select_stat.return_value = self.characters[0].stats[0]

        # Execute a sample event in the game and assert outcome
        event_result = self.game.current_event.execute(self.characters, self.parser)
        self.assertIn(event_result, ["pass", "partial_pass", "fail"])

    def test_check_location_cleared(self):
        self.game.completed_docked_inside = True
        self.assertTrue(self.game.check_location_cleared())

    def test_end_game_on_failure(self):
        self.game.fail_count = 5
        self.game.end_game()
        self.assertTrue(self.game.is_game_over)

    @patch('project_code.display_winning_crawl')
    def test_end_game_on_success(self, mock_winning_crawl):
        self.game.resolve_event("pass", Event({"id": "escape_star_destroyer"}))
        self.assertTrue(self.game.is_game_over)
        mock_winning_crawl.assert_called_once()


if __name__ == '__main__':
    unittest.main()

# # Add the root directory of the project to the Python path
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# from project_code.src.main import Statistic, Character, Jedi, BountyHunter, Droid, Event, EventStatus, display_opening_crawl, display_star_destroyer_prompt, display_winning_crawl
# from project_code.src.opening_crawl import display_opening_crawl
# from project_code.src.star_destroyer_prompt import display_star_destroyer_prompt
# from project_code.src.display_winning_crawl import display_winning_crawl

# import unittest

# class TestStatistic(unittest.TestCase):

#     def setUp(self):
#         self.strength = Statistic("Strength", description="Strength measures physical power.")

#     def test_statistic_initialization(self):
#         self.assertEqual(self.strength.name, "Strength")
#         self.assertEqual(self.strength.description, "Strength measures physical power.")

#     def test_statistic_str_method(self):
#         self.assertEqual(str(self.strength), "Strength")


# class TestCharacter(unittest.TestCase):

#     def setUp(self):
#         self.character = Character(name="Hero")

#     def test_character_initialization(self):
#         self.assertEqual(self.character.name, "Hero")
#         self.assertEqual(self.character.stats[0].name, "Strength")
#         self.assertEqual(self.character.stats[1].name, "Intelligence")

#     def test_character_stats_names(self):
#         stats_names = [str(stat) for stat in self.character.stats]
#         self.assertIn("Strength", stats_names)
#         self.assertIn("Intelligence", stats_names)


# class TestJedi(unittest.TestCase):

#     def setUp(self):
#         self.jedi = Jedi(name="Luke")

#     def test_jedi_initialization(self):
#         self.assertEqual(self.jedi.name, "Luke")
#         self.assertEqual(self.jedi.stats[2].name, "Force Sensitivity")
#         self.assertEqual(self.jedi.stats[3].name, "Mind Tricks")
#         self.assertEqual(self.jedi.stats[4].name, "Lightsaber Proficiency")


# class TestBountyHunter(unittest.TestCase):

#     def setUp(self):
#         self.bounty_hunter = BountyHunter(name="Han Solo")

#     def test_bounty_hunter_initialization(self):
#         self.assertEqual(self.bounty_hunter.name, "Han Solo")
#         self.assertEqual(self.bounty_hunter.stats[2].name, "Dexterity")
#         self.assertEqual(self.bounty_hunter.stats[3].name, "Blaster Proficiency")
#         self.assertEqual(self.bounty_hunter.stats[4].name, "Piloting")


# class TestDroid(unittest.TestCase):

#     def setUp(self):
#         self.droid = Droid(name="R2-D2")

#     def test_droid_initialization(self):
#         self.assertEqual(self.droid.name, "R2-D2")
#         self.assertEqual(self.droid.stats[2].name, "Processing")
#         self.assertEqual(self.droid.stats[3].name, "Hacking")


# class TestEvent(unittest.TestCase):

#     def setUp(self):
#         self.event_data = {
#             "id": "test_event",
#             "passing_attributes": {"Intelligence": "You solved the puzzle."},
#             "partial_pass_attributes": {"Strength": "You forced the door open halfway."},
#             "prompt_text": "A door blocks your path, covered in puzzles.",
#             "fail": {"message": "You couldn't open the door."},
#             "outcomes": {"pass": ["next_event"], "partial_pass": ["another_event"], "fail": ["retry_event"]}
#         }
#         self.event = Event(self.event_data)

#     def test_event_initialization(self):
#         self.assertEqual(self.event.name, "test_event")
#         self.assertEqual(self.event.prompt_text, "A door blocks your path, covered in puzzles.")
#         self.assertEqual(self.event.fail_message, "You couldn't open the door.")
#         self.assertEqual(self.event.outcomes["pass"], ["next_event"])

#     def test_event_resolve_choice_pass(self):
#         mock_character = Character()
#         mock_character.stats[1].name = "Intelligence"  # Set stat to match pass condition
#         self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[1]), EventStatus.PASS)

#     def test_event_resolve_choice_partial_pass(self):
#         mock_character = Character()
#         mock_character.stats[0].name = "Strength"  # Set stat to match partial pass condition
#         self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[0]), EventStatus.PARTIAL_PASS)

#     def test_event_resolve_choice_fail(self):
#         mock_character = Character()
#         mock_character.stats[0].name = "Dexterity"  # Set stat to trigger fail condition
#         self.assertEqual(self.event.resolve_choice(mock_character, mock_character.stats[0]), EventStatus.FAIL)


# if __name__ == '__main__':
#     unittest.main()
