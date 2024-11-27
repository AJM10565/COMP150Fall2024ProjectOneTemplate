import json
import os
import random
from enum import Enum
from typing import List
from flask import Flask, render_template, jsonify, request


# Flask App Initialization
app = Flask(__name__, static_folder="static", template_folder="templates")

# Enums and Core Classes
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

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))

    def __str__(self):
        return f"{self.name}: {self.value}"

class Character:
    def __init__(self, name: str, health: int = 100, strength: int = 10):
        self.name = name
        self.health = health
        self.strength = Statistic("Strength", value=strength, description="Physical power.")
        self.krabby_patties = 0
        self.weapon = "None"

    def collect_krabby_patties(self, amount: int):
        self.krabby_patties += amount

    def spend_krabby_patties(self, amount: int) -> bool:
        if self.krabby_patties >= amount:
            self.krabby_patties -= amount
            return True
        return False

class Game:
    def __init__(self, characters: List[Character], riddles: List[dict]):
        self.characters = characters
        self.riddles = riddles  # List of riddles
        self.used_riddles = set()
        self.correct_answers = 0
        self.current_riddle_index = 0  # Track the current riddle being asked

    def get_unused_riddle(self):
        # Get the next riddle in line (ignoring used riddles)
        if self.current_riddle_index < len(self.riddles):
            riddle = self.riddles[self.current_riddle_index]
            self.current_riddle_index += 1  # Move to the next riddle after this one
            return riddle
        return None  # No more riddles left

    def check_answer(self, choice_index: int, riddle: dict):
        # Check if the player's choice is correct
        return choice_index == riddle["correct_answer"]
def start(self):
     self.introduce_game()

     while self.continue_playing:
         riddle = self.get_unused_riddle()
         if not riddle:
             print("\nYou've solved all available riddles!")
             self.choose_path()
             break

         # Start the event (which might be a riddle or other action)
         event = Event(riddle)  # assuming riddle is structured for Event
         event.execute(self.party, self.parser)
         if self.correct_answers >= 3:
             self.choose_path()


# Flask Routes
player = Character(name="SpongeBob")
game = None

def initialize_game():
    global game
    data_path = os.path.join("data", "riddles.json")
    if not os.path.exists(data_path):
        print(f"Error: '{data_path}' not found.")
        game = None
    else:
        with open(data_path, "r") as file:
            riddles = json.load(file)
        game = Game([player], riddles)

initialize_game()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    if game is None:
        return jsonify({"message": "Game not initialized!"}), 500
    
    riddle = game.get_unused_riddle()  # Get a riddle
    if riddle:
        return jsonify({
            "message": "Game started! Good luck in Bikini Bottom!",
            "riddle_question": riddle["riddle_question"],
            "riddle_options": riddle["riddle_options"]
        })
    else:
        return jsonify({"message": "No riddles left!"}), 500



@app.route("/next", methods=["POST"])
def next_step():
    if game is None:
        return jsonify({"message": "Game not initialized!"}), 500
    return jsonify({"message": "Next step triggered! Check the console for progress."})


@app.route("/choice", methods=["POST"])
def make_choice():
    if game is None:
        return jsonify({"message": "Game not initialized!"}), 500
    
    data = request.json
    choice = data.get("choice", -1)  # The player's answer (index of the option)
    riddle = game.get_unused_riddle()
    
    if riddle:
        correct_answer = riddle["correct_answer"]
        if choice == correct_answer:
            message = "Correct! Well done."
        else:
            message = f"Incorrect! Your answer: '{riddle['riddle_options'][choice]}' Try again."
        
        # Get next riddle
        next_riddle = game.get_unused_riddle()
        if next_riddle:
            return jsonify({
                "message": message,
                "riddle_question": next_riddle["riddle_question"],
                "riddle_options": next_riddle["riddle_options"]
            })
        else:
            return jsonify({"message": message, "riddle_question": "No more riddles left!"})

    return jsonify({"message": "Error processing your choice!"}), 500

if __name__ == "__main__":
    app.run(debug=True)
