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
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str, health: int = 100, strength: int = 10):
        self.name = name
        self.health = health
        self.strength = Statistic("Strength", value=strength, description="Strength is a measure of physical power.")
        self.krabby_patties = 0
        self.weapon = "None"
        self.has_secret_formula = False

    def collect_krabby_patties(self, amount: int):
        self.krabby_patties += amount
        print(f"{self.name} collected {amount} Krabby Patties! Total: {self.krabby_patties}")

    def spend_krabby_patties(self, amount: int):
        if self.krabby_patties >= amount:
            self.krabby_patties -= amount
            return True
        else:
            print(f"Not enough Krabby Patties! {self.name} has {self.krabby_patties}, but {amount} is needed.")
            return False

    def __str__(self):
        return f"Character: {self.name}, Health: {self.health}, Strength: {self.strength}, Krabby Patties: {self.krabby_patties}, Weapon: {self.weapon}"