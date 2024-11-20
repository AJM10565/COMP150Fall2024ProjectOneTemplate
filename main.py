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
        self.riddles = riddles
        self.used_riddles = set()
        self.correct_answers = 0

    def get_unused_riddle(self):
        unused = [r for i, r in enumerate(self.riddles) if i not in self.used_riddles]
        if not unused:
            return None
        riddle = random.choice(unused)
        self.used_riddles.add(self.riddles.index(riddle))
        return riddle

    def collect_krabby_patties(self):
        for character in self.characters:
            amount = random.randint(1, 5)
            character.collect_krabby_patties(amount)

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
    return jsonify({"message": "Game started! Good luck in Bikini Bottom!"})

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
    choice = data.get("choice", "No choice provided")
    return jsonify({"message": f"Choice {choice} registered!"})

if __name__ == "__main__":
    app.run(debug=True)
