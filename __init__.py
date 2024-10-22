class Character:
    def __init__(self, name, character_class, health, strength):
        self.name = name
        self.character_class = character_class
        self.health = health
        self.strength = strength

    def __str__(self):
        return f"{self.name} the {self.character_class} (Health: {self.health}, Strength: {self.strength})"



class MrKrabs:
    def __init__(self):
        self.name = "Mr. Krabs"
        self.health = 150
        self.strength = 20  # Added strength for Mr. Krabs


def create_character():
    print("Welcome to Bikini Bottom! Choose your character:")
    characters = {
        "spongebob": ("SpongeBob SquarePants", 120, 15),
        "patrick": ("Patrick Star", 150, 10),
        "pearl": ("Pearl Krabs", 100, 12),
        "plankton": ("Plankton", 80, 8),
        "squidward": ("Squidward Tentacles", 90, 10)
    }

    for key, (name, health, strength) in characters.items():
        print(f"{key.capitalize()}: {name} (Health: {health}, Strength: {strength})")

    choice = input("Enter the name of your character: ").lower()

    if choice in characters:
        name, health, strength = characters[choice]
        player = Character(name, choice.capitalize(), health, strength)
        print(f"You have chosen: {player}")
        return player
    else:
        print("Invalid choice. Please choose a valid character.")
        return create_character()


def main():
    player = create_character()
    mr_krabs = MrKrabs()
    print(f"Your boss is: {mr_krabs.name} (Health: {mr_krabs.health}, Strength: {mr_krabs.strength})")

if __name__ == "__main__":
    main()
