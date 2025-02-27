import unittest
from unittest.mock import patch
from io import StringIO
from animal import Animal
from victim import Victim
from predator import Predator

class TestPredator(unittest.TestCase):
    def setUp(self):
        """Инициализация объекта Predator перед каждым тестом"""
        self.predator = Predator("Lion", "Panthera leo")
        self.victim = Victim("Deer", "Cervidae")

    def test_initialization(self):
        """Тестирование корректности инициализации"""
        self.assertEqual(self.predator.name, "Lion")
        self.assertEqual(self.predator.species, "Panthera leo")
        self.assertEqual(self.predator.energy, 100)
        self.assertEqual(self.predator.health, 100)

    def test_eat_victim(self):
        """Тестирование поедания жертвы"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.predator.eat(self.victim)
            self.assertIn("Lion is eating Deer", fake_out.getvalue())
            self.assertEqual(self.predator.energy, 120)
            self.assertEqual(self.victim.health, 0)

    def test_eat_non_victim(self):
        """Тестирование попытки съесть не-жертву"""
        non_victim = Animal("Grass", "Poaceae")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.predator.eat(non_victim)
            self.assertIn("Lion cannot eat Grass", fake_out.getvalue())
            self.assertEqual(self.predator.energy, 100)

    def test_hunt_success(self):
        """Тестирование успешной охоты"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.predator.hunt()
            self.assertIn("Lion is hunting", fake_out.getvalue())

    def test_hunt_failure(self):
        """Тестирование неудачной охоты (недостаточно энергии)"""
        self.predator.energy = 5
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.predator.hunt()
            self.assertIn("not enough energy", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()