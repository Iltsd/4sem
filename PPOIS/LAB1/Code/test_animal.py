import unittest
from unittest.mock import patch
from io import StringIO
from animal import Animal
from test_plant import TestPlant
from test_victim import TestVictim
from test_predator import TestPredator
from test_foodChain import TestFoodChain
from test_bioDiversity import TestBioDiversity
from test_ecoSystem import  TestEcosystem


class TestAnimal(unittest.TestCase):
    def setUp(self):
        self.animal = Animal("Simba", "Lion")

    def test_initialization(self):
        """Тестирование корректности инициализации"""
        self.assertEqual(self.animal.name, "Simba")
        self.assertEqual(self.animal.species, "Lion")
        self.assertEqual(self.animal.energy, 100)
        self.assertEqual(self.animal.health, 100)

    def test_reproduce_success(self):
        """Тестирование успешного размножения"""
        baby = self.animal.reproduce()
        self.assertIsInstance(baby, Animal)
        self.assertEqual(baby.name, "Baby Simba")
        self.assertEqual(self.animal.energy, 50)

    def test_reproduce_failure(self):
        """Тестирование неудачного размножения"""
        self.animal.energy = 40
        with patch('sys.stdout', new=StringIO()) as fake_out:
            baby = self.animal.reproduce()
            self.assertIsNone(baby)
            self.assertIn("not have enough energy", fake_out.getvalue())
            self.assertEqual(self.animal.energy, 40)

    def test_die(self):
        """Тестирование метода смерти"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.animal.die()
            self.assertEqual(self.animal.health, 0)
            self.assertIn("has died", fake_out.getvalue())

    def test_defend_alive(self):
        """Тестирование защиты живого животного"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.animal.defend()
            self.assertIn("Still alive", fake_out.getvalue())

    def test_defend_dead(self):
        """Тестирование защиты мертвого животного"""
        self.animal.health = 0
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.animal.defend()
            self.assertEqual(fake_out.getvalue().strip(), "")

    def test_eat_not_implemented(self):
        """Тестирование выброса исключения для метода eat"""
        with self.assertRaises(NotImplementedError):
            self.animal.eat("food")


if __name__ == '__main__':
    unittest.main()