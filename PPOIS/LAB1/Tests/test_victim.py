import unittest
from unittest.mock import patch
from io import StringIO
from animal import Animal
from plant import Plant
from victim import Victim

class TestVictim(unittest.TestCase):
    def setUp(self):

        self.victim = Victim("Deer", "Cervidae")
        self.edible_plant = Plant("Grass", "Poaceae", True)
        self.poisonous_plant = Plant("Poison Ivy", "Toxicodendron", False)
        self.non_plant = Animal("Rock", "Mineral")

    def test_initialization(self):

        self.assertEqual(self.victim.name, "Deer")
        self.assertEqual(self.victim.species, "Cervidae")
        self.assertEqual(self.victim.energy, 100)
        self.assertEqual(self.victim.health, 100)

    def test_eat_edible_plant(self):

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.victim.eat(self.edible_plant)
            self.assertIn("Deer is eating Grass", fake_out.getvalue())
            self.assertEqual(self.victim.energy, 110)

    def test_eat_poisonous_plant(self):

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.victim.eat(self.poisonous_plant)
            self.assertIn("This plant is poisonous", fake_out.getvalue())
            self.assertEqual(self.victim.energy, 100)

    def test_eat_non_plant(self):

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.victim.eat(self.non_plant)
            self.assertIn("Deer cannot eat Rock", fake_out.getvalue())
            self.assertEqual(self.victim.energy, 100)

    def test_defend_success(self):

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.victim.defend()
            self.assertIn("Deer is running away from predators", fake_out.getvalue())

    def test_defend_failure(self):

        self.victim.energy = 5
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.victim.defend()
            self.assertIn("Deer has died", fake_out.getvalue())
            self.assertEqual(self.victim.health, 0)

if __name__ == '__main__':
    unittest.main()