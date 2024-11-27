from location_events.character import Character



class WeaponShop:
    def __init__(self):
        self.weapons = {
            "1. Spatula": 5,
            "2. Karen": 10,
            "3. Golden Spatula": 20
        }

    def display_weapons(self):
        print("Weapons available for purchase:")
        for weapon, cost in self.weapons.items():
            print(f"{weapon}: {cost} Krabby Patties")

    def purchase_weapon(self, character: Character):
        self.display_weapons()
        weapon_choice = input("Enter the number of the weapon you would like to buy (1-3): ")
        weapon_map = {
            "1": "1. Spatula",
            "2": "2. Karen",
            "3": "3. Golden Spatula"
        }
        if weapon_choice in weapon_map:
            weapon_name = weapon_map[weapon_choice]
            cost = self.weapons[weapon_name]
            if character.spend_krabby_patties(cost):
                character.weapon = weapon_name
                print(f"{character.name} purchased {weapon_name}!")
            else:
                print("Transaction failed. Not enough Krabby Patties.")
        else:
            print("Invalid choice.")


class UpgradeShop:
    def __init__(self):
        self.upgrades = {
            "1. Strength Upgrade": 5,
            "2. Health Upgrade": 5
        }

    def display_upgrades(self):
        print("Upgrades available for purchase:")
        for upgrade, cost in self.upgrades.items():
            print(f"{upgrade}: {cost} Krabby Patties")

    def purchase_upgrade(self, character: Character):
        self.display_upgrades()
        upgrade_choice = input("Enter the number of the upgrade you would like to buy (1-2): ")
        upgrade_map = {
            "1": "1. Strength Upgrade",
            "2": "2. Health Upgrade"
        }
        if upgrade_choice in upgrade_map:
            upgrade_name = upgrade_map[upgrade_choice]
            if character.spend_krabby_patties(self.upgrades[upgrade_name]):
                if upgrade_choice == "1":
                    character.strength.modify(5)
                    print(f"{character.name}'s strength increased to {character.strength.value}!")
                else:
                    character.health += 10
                    print(f"{character.name}'s health increased to {character.health}!")
        else:
            print("Invalid choice.")