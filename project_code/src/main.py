import json
import sys
import random
from typing import List, Optional
from enum import Enum

from project_code.src.display_winning_crawl import display_winning_crawl
from project_code.src.opening_crawl import display_opening_crawl
from project_code.src.star_destroyer_prompt import display_star_destroyer_prompt


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"

class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = ""):
        self.name = name
        self.value = value  # Retain this for use in other parts of the game
        self.description = description
        # Removed value, min_value, and max_value for displaying only names

    def __str__(self):
        return self.name  # Display only the name here


class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.stats = []
        # Initialize only statistic names without values
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        self.stats.extend([self.strength, self.intelligence])

    def get_stats(self):
        return self.stats

    def __str__(self):
        return ', '.join(str(stat) for stat in self.stats)  # Display only the names of the stats


# Jedi subclass
class Jedi(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.force_sensitivity = Statistic("Force Sensitivity", description="Force Sensitivity is a measure of proficiency in force strength.")
        self.mind_tricks = Statistic("Mind Tricks", description="Mind tricks is a measure of Jedi mind control.")
        self.lightsaber_proficiency = Statistic("Lightsaber Proficiency", description="Lightsaber proficiency is a measure of skill with a lightsaber.")
        self.stats.extend([self.force_sensitivity, self.mind_tricks, self.lightsaber_proficiency])


# Bounty Hunter subclass
class BountyHunter(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.dexterity = Statistic("Dexterity", description="Agility and precision.")
        self.blaster_proficiency = Statistic("Blaster Proficiency", description="Skill with ranged blaster weapons.")
        self.piloting = Statistic("Piloting", description="Skill in piloting ships and vehicles.")
        self.stats.extend([self.dexterity, self.blaster_proficiency, self.piloting])


# Droid subclass
class Droid(Character):
    def __init__(self, name: str = "Bob"):
        super().__init__(name)
        self.processing = Statistic("Processing", description="Ability to process information effectively.")
        self.hacking = Statistic("Hacking", description="Ability to hack gateways and doors.")
        self.stats.extend([self.processing, self.hacking])


class Event:
    def __init__(self, data: dict):
        self.name = data.get("id", "unknown_event")
        self.passing_attributes = data['passing_attributes']
        self.partial_pass_attributes = data['partial_pass_attributes']
        self.prompt_text = data['prompt_text']
        self.fail_message = data['fail']['message']
        self.outcomes = data['outcomes']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        outcome = self.resolve_choice(character, chosen_stat)
        # Print based on the outcome
        if outcome == EventStatus.FAIL:
            print(self.fail_message)
        elif outcome == EventStatus.PARTIAL_PASS:
            print(self.partial_pass_attributes[chosen_stat.name])
        else:
            print(self.passing_attributes[chosen_stat.name])
        
        # Return the outcome's value (either "pass", "partial_pass", or "fail")
        return outcome.value

    def resolve_choice(self, character: Character, chosen_stat: Statistic) -> EventStatus:
        """This will check if the stat selected pass, partial pass, or fails the event."""
        # Check for pass, partial pass, or fail based on the chosen stat
        if chosen_stat.name in self.passing_attributes:
            self.status = EventStatus.PASS
        elif chosen_stat.name in self.partial_pass_attributes:
            self.status = EventStatus.PARTIAL_PASS
        else:
            self.status = EventStatus.FAIL

        # Return the status, which will help `execute` print the correct messages
        return self.status
    
    def get_next_location(self):
        """Determine the next location based on the event's status."""
        if self.status == EventStatus.PASS:
            return random.choice(self.outcomes["pass"])
        elif self.status == EventStatus.PARTIAL_PASS:
            return random.choice(self.outcomes["partial_pass"])
        else:
            return random.choice(self.outcomes["fail"])




class Location:
    def __init__(self, name: str, events: List[Event]):
        self.name = name
        self.events = events
        self.used_events = []   # Keep track of used events
    
    def get_event(self, event_name) -> Event:
        if len(self.events) == 0:
            # Reset used events if all have been used
            self.events, self.used_events = self.used_events, []

        for event in self.events:
            if event.name == event_name:
                return event
        else:
            event = random.choice(self.events)  # Randomly choose an event
            self.events.remove(event)  # Remove it from the available events
            self.used_events.append(event)  # Track that this event has been used
            return event


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location], max_failures):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.current_location = locations[0]  # Start at the first location (Jedha)
        self.unlocked_star_destroyer = False
        self.fail_count = 0
        self.max_failures = max_failures
        self.is_game_over = False
        self.completed_docked_inside = False

        self.current_event = self.current_location.get_event("Beginning")
    
    def start(self):
        while not self.is_game_over:
            event_result = self.current_event.execute(self.party, self.parser)
            self.resolve_event(event_result, self.current_event)

            # Check if location is cleared and transition if needed            
            if self.check_location_cleared() and not self.is_game_over:                
                self.transition_to_star_destroyer()
                self.current_event = self.current_location.get_event("hanger")

            # Get the next event based on the outcome of the current event            
            next_event_name = self.current_event.get_next_location()            
            self.current_event = self.current_location.get_event(next_event_name)


    def transition_to_star_destroyer(self):
        print("You've cleared all events on Jedha. You can now board the Star Destroyer.")
        display_star_destroyer_prompt()
        self.current_location = self.locations[1]  # Move to the Star Destroyer


    def resolve_event(self, event_result: str, event: Event):
        """Increment failure count if the event fails and end the game if max failures are reached."""
        if event_result == EventStatus.FAIL.value:
            self.fail_count += 1
            print(f"Failure count: {self.fail_count}/{self.max_failures}")
            if self.fail_count >= self.max_failures:    # Check if the failure threshold is reached
                self.end_game()

        if event.name == "escape_star_destroyer" and event_result == "pass" or event.name == "escape_star_destroyer" and event_result == "partial_pass":
            """End game when won"""
            self.is_game_over = True
            display_winning_crawl()  # Call the winning crawl when the game is won


        if event.name == "escape_star_destroyer" and event_result == "fail":
            """End game when won"""
            self.is_game_over = True
            print("You fail to escape, and the bombs go off with you inside the Star Destroyer. GAME OVER")        


        if event.name == "docked_inside" and event_result == "pass":
            self.completed_docked_inside = True

    def check_location_cleared(self):
        # Location is cleared if "docked_inside" has been passed
        return self.completed_docked_inside and self.current_location.name == "Jedha"

    def end_game(self):
        """End the game if the failure threshold is met or if the player wins."""
        self.is_game_over = True
        if self.fail_count >= self.max_failures:
            print("Game Over: You've failed too many events.")

    
class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_characters(self, available_characters: List[Character], num_choices: int = 3) -> List[Character]:
        """Allows the player to select a specific number of characters from the list to form the party."""
        if len(available_characters) < num_choices:
            raise ValueError(f"Not enough available characters to select {num_choices}.")

        chosen_characters = []
        print("Select 3 characters to form your party:")

        for idx, character in enumerate(available_characters):
            print(f"{idx + 1}. {character.name} - {type(character).__name__}")

        while len(chosen_characters) < num_choices:
            try:
                choice = int(self.parse("Enter the number of the character to select: ")) - 1
                if 0 <= choice < len(available_characters):
                    if available_characters[choice] not in chosen_characters:
                        chosen_characters.append(available_characters[choice])
                        print(f"{available_characters[choice].name} has been added to your party.")
                    else:
                        print("You have already selected that character. Please choose another.")
                else:
                    print("Invalid selection. Please choose a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        return chosen_characters

    def select_party_member(self, party: List[Character], num_options: int = 3) -> Character:
        """Allows the player to choose a party member from a list of up to num_options members."""
        displayed_party = party if len(party) <= num_options else random.sample(party, num_options)

        print("Choose a party member:")
        for idx, member in enumerate(displayed_party):
            print(f"{idx + 1}. {member.name}")

        while True:
            try:
                choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
                if 0 <= choice < len(displayed_party):
                    return displayed_party[choice]
                else:
                    print("Invalid selection. Please choose again.")
            except ValueError:
                print("Please enter a valid number.")



    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name}")
        # Loop until a valid input is entered
        while True:
            try:
                choice = int(self.parse("Enter the number of the stat to use: ")) - 1
                if 0 <= choice < len(stats):
                    return stats[choice]
                else:
                    print(f"Invalid selection. Please choose a number between 1 and {len(stats)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")



def load_events_from_json(file_path: str) -> List[Event]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Event(event_data) for event_data in data]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []


# from opening_crawl import display_opening_crawl
# from star_destroyer_prompt import display_star_destroyer_prompt
# from display_winning_crawl import display_winning_crawl

def start_game():
    display_opening_crawl()
    parser = UserInputParser()

    #Creating a character list 
    all_characters = [
        Jedi("Luke"),
        Jedi("Obi-wan"),
        BountyHunter("Han Solo"),
        BountyHunter("Chewbacca"),
        BountyHunter("Lando Calrissian"),
        Character("Princess Leia"),
        Character("Poe Dameron"),
        Droid("C-3PO"),
        Droid("R2-D2"),
    ]
    
    selected_characters = parser.select_characters(all_characters)



    jedha_events = load_events_from_json('project_code/location_events/jedha_events.json')
    star_destroyer_events = load_events_from_json('project_code/location_events/star_destroyer_events.json')
    
    locations = [
        Location("Jedha", jedha_events),
        Location("Star Destroyer", star_destroyer_events)
    ]


    game = Game(parser, selected_characters, locations, max_failures=5)
    game.start()


if __name__ == '__main__':
    start_game()

