import json
import sys
import random
from typing import List, Optional
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value


    def __str__(self):
        return f"{self.name}: {self.value}"  # Display the correct value here

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str = "Bob", strength_value: int = 10, intelligence_value: int = 10):
        self.name = name
        self.stats = []
        self.strength = Statistic("Strength", 10, description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", 10, description="Intelligence is a measure of cognitive ability.")
        self.stats.extend([self.strength, self.intelligence])
        # Add more stats as needed
        #we added a new subclass and talked about our plan for the future in the ic

    def get_stats(self):
        return self.stats

#jedi subclass
class Jedi(Character):
    def __init__(self, name: str):
        super().__init__(name, strength_value=60, intelligence_value=80)
        self.force_sensitivity = Statistic("Force Sensitivity", 60, description="Force Sensitivity is a measure of proficiency in force strength.")
        self.mind_tricks = Statistic("Mind Tricks", 60, description="Mind tricks is a measure of jedi mind control.")
        self.lightsaber_proficiency = Statistic("Lightsaber Proficiency", 80, description="Lightsaber proficiency is a measure of skill with a lightsaber.")
        self.stats.extend([self.force_sensitivity, self.mind_tricks, self.lightsaber_proficiency])

#added a bounty hunter subclass
class BountyHunter(Character):
    def __init__(self, name: str):
        super().__init__(name, strength_value=50, intelligence_value=50)
        self.dexterity = Statistic("Dexterity", 65, description="Agility and precision.")
        self.blaster_proficiency = Statistic("Blaster Proficiency", 70, description="Skill with ranged blaster weapons.")
        self.piloting = Statistic("Piloting", 60, description="Skill in piloting ships and vehicles.")
        self.stats.extend([self.dexterity, self.blaster_proficiency, self.piloting])

#droid subclass
class Droid(Character):
    def __init__(self, name: str = "Bob"):
        super().__init__(name, strength_value=30, intelligence_value=80)
        self.processing = Statistic("Processing", 85, description="Ability to processess information effectively.")
        self.hacking = Statistic("Hacking", 70, description="Ability to hack gateways and doors.")
        self.stats.extend([self.processing, self.hacking])


# Example of how to create and print these characters
# jedi_character = Jedi(name="Obi-Wan Kenobi")
# bounty_hunter_character = BountyHunter(name="Boba Fett")


class Event:
    def __init__(self, data: dict):
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
        self.resolve_choice(character, chosen_stat)
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
    
    def get_event(self) -> Event:
        if len(self.events) == 0:
            #Rest used events if all have been used
            self.events, self.used_events = self.used_events, []
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

    def start(self):
        while not self.is_game_over:
            event = self.current_location.get_event()
            event_result = event.execute(self.party, self.parser)

            # Resolve the event's outcome
            self.resolve_event(event_result)

            # Check if location is cleared and transition if needed
            if self.check_location_cleared() and not self.is_game_over:
                self.transition_to_star_destroyer()

    def check_location_cleared(self):
        # If all events in the current location are completed
        return len(self.current_location.events) == 0 and self.current_location.name == "Jedha"

    def transition_to_star_destroyer(self):
        print("You've cleared all events on Jedha. You can now board the Star Destroyer.")
        self.current_location = self.locations[1]  # Move to the Star Destroyer

    def resolve_event(self, event_result: str):
        """Increment failure count if the event fails and end the game if max failures are reached."""
        if event_result == "fail":
            self.fail_count += 1
            print(f"Failure count: {self.fail_count}/{self.max_failures}")

            # Check if the failure threshold is reached
            if self.fail_count >= self.max_failures:
                self.end_game()

    def end_game(self):
        """End the game if the failure threshold is met."""
        self.is_game_over = True
        print("Game Over: You've failed too many events.")
    

class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)
    
    def select_party_member(self,party: List[Character], num_options: int = 3) -> Character:
        #selects a random subset of the party to display as options 
        if len(party) <= num_options: 
            displayed_party = party 
        else: 
            displayed_party = random.sample(party, num_options)

        #Displays options
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
            print(f"{idx + 1}. {stat.name} ({stat.value})")
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



def start_game():
    parser = UserInputParser()

    #Creating a character list 
    characters = [
        Jedi("Luke"),
        Jedi("Obi-wan"),
        BountyHunter("Han Solo"),
        BountyHunter("Chewbacca"),
        BountyHunter("Lando Calrissian"),
        Character("Princess Leia"),
        Droid("C3PO"),
        Droid("R2-D2"),
        ]
    
    selected_characters = random.sample(characters, 3)


    jedha_events = load_events_from_json('project_code/location_events/jedha_events.json')
    star_destroyer_events = load_events_from_json('project_code/location_events/star_destroyer_events.json')
    
    locations = [
        Location("Jedha", jedha_events),
        Location("Star Destroyer", star_destroyer_events)
    ]


    game = Game(parser, selected_characters, locations, max_failures = 3)
    game.start()


if __name__ == '__main__':
    start_game()

