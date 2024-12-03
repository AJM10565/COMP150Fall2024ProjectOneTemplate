
import random
from typing import List
import random
from character import Character, EventStatus, Statistic
from parser import Parser


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.riddle_question = data.get('riddle_question', '')
        self.riddle_options = data.get('riddle_options', [])
        self.correct_answer = data.get('correct_answer', -1)
        self.status = EventStatus.UNKNOWN

        # Randomize the riddle options and update the correct answer index
        self.shuffle_riddle_options()

    def shuffle_riddle_options(self):
        # If there are no options or only one, we don't need to shuffle
        if len(self.riddle_options) > 1:
            # Randomly shuffle the riddle options
            correct_option = self.riddle_options[self.correct_answer]  # Save the correct answer
            random.shuffle(self.riddle_options)  # Shuffle all options

            # After shuffling, find the new index of the correct answer
            self.correct_answer = self.riddle_options.index(correct_option)

    def execute(self, party: List[Character], parser: Parser):
        if self.riddle_question:
            self.ask_riddle(parser)
            return

        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def ask_riddle(self, parser: Parser):
        print(self.riddle_question)
        user_choice = parser.select_riddle_option(self.riddle_options)

        if user_choice.isdigit() and 0 <= int(user_choice)-1 < len(self.riddle_options) and int(user_choice)-1 == self.correct_answer:
            print("You solved the riddle and pushed the door open. You may proceed.")
            self.status = EventStatus.PASS
        else:
            print("Wrong answer! The door remains closed.")
            self.status = EventStatus.FAIL

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print("You successfully used your strength!")
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print("You made some progress, but not enough!")
        else:
            self.status = EventStatus.FAIL
            print("You failed to achieve your goal.")