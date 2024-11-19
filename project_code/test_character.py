import unittest
from location_events.character import Character, Statistic

class TestCharacter(unittest.TestCase):

    def test_collect_krabby_patties(self):
        spongebob = Character("SpongeBob")
        spongebob.collect_krabby_patties(5)
        self.assertEqual(spongebob.krabby_patties, 5)

    def test_spend_krabby_patties(self):
        spongebob = Character("SpongeBob")
        spongebob.krabby_patties = 10
        self.assertTrue(spongebob.spend_krabby_patties(5))
        self.assertEqual(spongebob.krabby_patties, 5)

    def test_spend_krabby_patties_insufficient(self):
        spongebob = Character("SpongeBob")
        spongebob.krabby_patties = 5
        self.assertFalse(spongebob.spend_krabby_patties(10))

    def test_modify_strength(self):
        spongebob = Character("SpongeBob")
        spongebob.strength.modify(5)
        self.assertEqual(spongebob.strength.value, 15)

    def test_modify_strength_max(self):
        spongebob = Character("SpongeBob")
        spongebob.strength.modify(100)
        self.assertEqual(spongebob.strength.value, 100)

    def test_modify_strength_min(self):
        spongebob = Character("SpongeBob")
        spongebob.strength.modify(-10)
        self.assertEqual(spongebob.strength.value, 0)

if __name__ == "__main__":
    unittest.main()