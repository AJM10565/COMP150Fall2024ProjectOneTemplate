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
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        """This will check if the stat selected pass, partial pass, or fails the event"""
        #pass
        if chosen_stat.name in self.passing_attributes:
            self.status = EventStatus.PASS
            print(self.passing_attributes[chosen_stat.name])
        #partial pass
        elif chosen_stat.name in self.partial_pass_attributes:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_attributes[chosen_stat.name])
        #fail
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


class StatisticGrantEvent(Event):
    def __init__(self, data: dict):
        super().__init__(data)
        self.stat_to_grant = data['stat_to_grant']  # The existing stat to add from the subclass
    
    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        super().resolve_choice(character, chosen_stat)
        # If the event is passed, try to grant the new stat
        if self.status == EventStatus.PASS:
            self.grant_existing_stat(character)

    def grant_existing_stat(self, character: Character):
        # Check if the stat to be granted already exists in the character
        if any(stat.name == self.stat_to_grant for stat in character.stats):
            print(f"{character.name} already has the stat: {self.stat_to_grant}")
            return
        
        # Check if the stat exists in the character's subclass
        stat_to_add = self.get_stat_from_subclass(character, self.stat_to_grant)
        
        if stat_to_add:
            character.stats.append(stat_to_add)
            print(f"{character.name} gained a new stat: {stat_to_add.name} with value {stat_to_add.value}")
        else:
            print(f"Stat {self.stat_to_grant} not found in {character.name}'s class.")
    
    def get_stat_from_subclass(self, character: Character, stat_name: str) -> Optional[Statistic]:
        """
        This method tries to find the specified stat from the character's subclass.
        Returns the matching Statistic object or None if not found.
        """
        subclass_stats = []
        
        # Check for Jedi subclass
        if isinstance(character, Jedi):
            subclass_stats = [
                character.force_sensitivity,
                character.mind_tricks,
                character.lightsaber_proficiency
            ]
        # Check for BountyHunter subclass
        elif isinstance(character, BountyHunter):
            subclass_stats = [
                character.dexterity,
                character.blaster_proficiency,
                character.piloting
            ]
        # Check for Droid subclass
        elif isinstance(character, Droid):
            subclass_stats = [
                character.processing,
                character.hacking
            ]
        
        # Find and return the stat from the subclass
        for stat in subclass_stats:
            if stat.name == stat_name:
                return stat
        
        return None


    
class Location:
    def __init__(self, events: List[Event]):
        self.events = events
        self.used_events = []  # Keep track of used events

    def get_event(self) -> Event:
        if len(self.events) == 0:
            # Reset used events if all have been used
            self.events, self.used_events = self.used_events, []
        
        event = random.choice(self.events)  # Randomly choose an event
        self.events.remove(event)  # Remove it from the available events
        self.used_events.append(event)  # Track that this event has been used
        return event



class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True

    def start(self):
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False
        print("Game Over.")

    def check_game_over(self):
        return len(self.party) == 0


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
    with open(file_path, 'r') as file:
        data = json.load(file)

    events = []
    for event_data in data:
        if event_data.get('stat_to_grant'):  
            events.append(StatisticGrantEvent(event_data))
        else:
            events.append(Event(event_data))
    return events



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

    events = load_events_from_json('project_code/location_events/location_1.json')
    
    locations = [Location(events)]
    game = Game(parser, selected_characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()
