from typing import List
from character import Character, Statistic

class Parser:
    def select_party_member(self, party: List[Character]) -> Character:
        return party[0]

    def select_stat(self, character: Character) -> Statistic:
        return character.strength

    def select_riddle_option(self, options: List[str]) -> str:
        for i, option in enumerate(options, 1):
            print(option)
        return input("Enter the number of your answer (1-3): ")