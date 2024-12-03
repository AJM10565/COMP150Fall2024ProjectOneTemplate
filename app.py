import json
import os
from typing import List
from flask import Flask, render_template, jsonify, request
import sys
import random

# Add the location_events directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'location_events'))

from location_events.character import Character
from location_events.game import Game
from location_events.location import Location
from location_events.parser import Parser
from location_events.shop import WeaponShop

app = Flask(__name__, static_folder="static", template_folder="templates")

# Corrected path to riddles.json
data_path = os.path.join(os.path.dirname(__file__), "location_events", "data", "riddles.json")

# Check if the file exists
if not os.path.exists(data_path):
    print(f"Error: The file {data_path} does not exist!")
else:
    print(f"Found riddles.json at: {data_path}")

# Function to get the file path
def get_project_file_path(*path_parts):
    return os.path.join(os.path.dirname(__file__), *path_parts)

locations_path = get_project_file_path("locations.json")

# Initialize game variables
game = None  # Initialize the game object
player = None  # Initialize the player character
parser = Parser()  # Initialize the parser

# Initialize riddle variables
player_riddle_count = 0
player_krabby_patties = 0
player_weapon = "None"

riddles = [
    {"question": "What has to be broken before you can use it?", "options": ["Egg", "Window", "Lock"], "answer": 0},
    {"question": "What is yellow and dangerous?", "options": ["Banana", "Electric Eel", "SpongeBob"], "answer": 1},
    {"question": "What can travel around the world while staying in the corner?", "options": ["Stamp", "Clock", "SpongeBob"], "answer": 0},
    {"question": "I’m tall when I’m young and short when I’m old. What am I?", "options": ["Candle", "Tree", "SpongeBob"], "answer": 0},
    {"question": "What has keys but can’t open locks?", "options": ["Piano", "Lock", "SpongeBob"], "answer": 0},
]

# Battle stats for Sandy Cheeks
sandy_health = 100
player_health = 100

def battle():
    global sandy_health
    damage = random.randint(10, 30)  # Player attacks Sandy
    sandy_health -= damage
    return sandy_health

def load_locations():
    """Load locations from a JSON file."""
    try:
        with open(locations_path, 'r') as file:
            location_data = json.load(file)
            locations = []
            for location_info in location_data['locations']:
                if isinstance(location_info, dict):
                    events = [Event(event_data) for event_data in location_info.get('events', [])]
                    locations.append(Location(location_info, events))
                else:
                    print(f"Invalid data structure in location: {location_info}")
            return locations
    except Exception as e:
        print(f"Error loading locations: {e}")
        return []

# Event class definition (added back)
class Event:
    def __init__(self, event_type):
        self.event_type = event_type
        if event_type == "riddle":
            self.riddle_question = "What has to be broken before you can use it?"
            self.riddle_options = ["Egg", "Window", "Lock"]
            self.correct_answer = 0  # Let's say "Egg" is correct
        elif event_type == "battle":
            self.riddle_question = "Time to battle!"
            self.riddle_options = []
            self.correct_answer = None  # No question for battle
        elif event_type == "shop":
            self.riddle_question = "Would you like to buy a weapon?"
            self.riddle_options = ["Yes", "No"]
            self.correct_answer = 0  # Assume Yes is the correct answer
        else:
            self.riddle_question = None
            self.riddle_options = []
            self.correct_answer = None

# Game class
class Game:
    def __init__(self, parser: Parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.characters = characters
        self.locations = locations or self.load_locations()  # Default to loading locations if none are provided
    
    def load_locations(self):
        """Load locations from the locations.json file."""
        try:
            with open(locations_path, 'r') as file:
                location_data = json.load(file)
                locations = []
                for location_info in location_data:
                    if isinstance(location_info, dict):  # Ensure location_info is a dictionary
                        events = [Event(event_data) for event_data in location_info.get('events', [])]
                        locations.append(Location(location_info, events))
                    else:
                        print(f"Invalid data structure in location: {location_info}")  # Debug log
                return locations
        except Exception as e:
            print(f"Error loading locations: {e}")
            return []

# Set up routes
@app.route('/')
def index():
    global game, player, player_riddle_count, player_krabby_patties, player_weapon, sandy_health, player_health
    
    # Reset game state variables for a fresh start
    player_riddle_count = 0
    player_krabby_patties = 0
    player_weapon = "None"
    sandy_health = 100
    player_health = 100
    
    if game is None:
        print("Initializing game...")  # Debug message
        player = Character("SpongeBob")
        game = Game(parser, [player], load_locations())  # Initialize game with locations
        print("Game initialized.")  # Debug message
    
    # Confirm the template is being rendered
    print("Rendering index page...")  # Debug message
    return render_template('index.html', krabbyPatties=player_krabby_patties, weapon=player_weapon)


# Routes for game logic
@app.route("/start", methods=["POST"])
def start_game():
    global player_riddle_count
    # Provide a riddle from the list
    riddle = riddles[player_riddle_count]
    return jsonify({
        "message": "Welcome to the game! Solve riddles to earn Krabby Patties and defeat Mr. Krabs and Sandy Cheeks!",
        "riddle_question": riddle["question"],
        "riddle_options": riddle["options"]
    })

@app.route("/next", methods=["POST"])
def next_step():
    global player_riddle_count
    if player_riddle_count < 3:
        player_riddle_count += 1
        riddle = riddles[player_riddle_count]
        return jsonify({
            "message": f"Correct! You have earned Krabby Patties. Your current Krabby Patties: {player_krabby_patties}",
            "riddle_question": riddle["question"],
            "riddle_options": riddle["options"]
        })
    else:
        # After 3 riddles, offer a choice
        return jsonify({
            "message": "You've solved 3 riddles! What do you want to do next?",
            "riddle_question": "Choose your action:",
            "riddle_options": ["Fight Sandy Cheeks", "Upgrade Weapon", "Keep Solving Riddles"]
        })

@app.route("/choice", methods=["POST"])
def make_choice():
    choice = request.json.get("choice")
    global player_krabby_patties, player_weapon, sandy_health, player_health

    if choice == 0:  # Fight Sandy Cheeks
        # Battle with Sandy Cheeks
        battle_message = f"Sandy Cheeks has {sandy_health} health left."
        while sandy_health > 0 and player_health > 0:
            sandy_health = battle()  # Player attacks Sandy
            player_health -= random.randint(5, 20)  # Sandy attacks player
            battle_message += f" You attack and deal damage! Your health: {player_health}, Sandy's health: {sandy_health}."
            if sandy_health <= 0:
                return jsonify({
                    "message": f"You defeated Sandy Cheeks! Your remaining health: {player_health}.",
                    "krabby_patties": player_krabby_patties,
                    "weapon": player_weapon
                })
            if player_health <= 0:
                return jsonify({
                    "message": "You were defeated by Sandy Cheeks. Try again!",
                    "krabby_patties": player_krabby_patties,
                    "weapon": player_weapon
                })
        return jsonify({
            "message": battle_message,
            "krabby_patties": player_krabby_patties,
            "weapon": player_weapon
        })
    elif choice == 1:  # Upgrade Weapon
        # Weapon upgrade logic
        player_weapon = "Laser Gun"  # For example
        return jsonify({
            "message": f"You upgraded your weapon to {player_weapon}!",
            "krabby_patties": player_krabby_patties,
            "weapon": player_weapon
        })
    elif choice == 2:  # Keep solving riddles
        # Solve another riddle
        riddle = riddles[player_riddle_count]
        return jsonify({
            "message": "Solving more riddles...",
            "riddle_question": riddle["question"],
            "riddle_options": riddle["options"]
        })

@app.route("/solve_riddle", methods=["POST"])
def solve_riddle():
    global player_krabby_patties
    answer = request.json.get("answer")
    riddle = riddles[player_riddle_count]

    if answer == riddle["answer"]:
        player_krabby_patties += 10  # Earn Krabby Patties
        return jsonify({
            "message": f"Correct! You earned 10 Krabby Patties. Your total: {player_krabby_patties}",
            "riddle_question": riddle["question"],
            "riddle_options": riddle["options"]
        })
    else:
        return jsonify({
            "message": "Incorrect! Try again.",
            "riddle_question": riddle["question"],
            "riddle_options": riddle["options"]
        })

if __name__ == '__main__':
    app.run(debug=True)
