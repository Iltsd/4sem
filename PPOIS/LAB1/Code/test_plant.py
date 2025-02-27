import unittest
from unittest.mock import patch
from io import StringIO
from plant import Plant

class TestPlant(unittest.TestCase):
    def setUp(self):
        """Инициализация объекта Plant перед каждым тестом"""
        self.plant = Plant("Oak", "Quercus", is_edible=True)

    def test_initialization(self):
        """Тестирование корректности инициализации"""
        self.assertEqual(self.plant.name, "Oak")
        self.assertEqual(self.plant.species, "Quercus")
        self.assertTrue(self.plant.is_edible)
        self.assertEqual(self.plant.health, 100)

    def test_grow(self):
        """Тестирование метода grow"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.plant.grow()
            self.assertIn("Oak is growing", fake_out.getvalue())
            self.assertEqual(self.plant.health, 110)

    def test_reproduce_success(self):
        """Тестирование успешного размножения"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            baby_plant = self.plant.reproduce()
            self.assertIsInstance(baby_plant, Plant)
            self.assertEqual(baby_plant.name, "Seedling of Oak")
            self.assertEqual(self.plant.health, 50)
            self.assertIn("Oak is reproducing", fake_out.getvalue())

    def test_reproduce_failure(self):
        """Тестирование неудачного размножения (недостаточно здоровья)"""
        self.plant.health = 40
        with patch('sys.stdout', new=StringIO()) as fake_out:
            baby_plant = self.plant.reproduce()
            self.assertIsNone(baby_plant)
            self.assertIn("Oak does not have enough health to reproduce", fake_out.getvalue())
            self.assertEqual(self.plant.health, 40)

    def test_die(self):
        """Тестирование метода die"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.plant.die()
            self.assertEqual(self.plant.health, 0)
            self.assertIn("Oak has died", fake_out.getvalue())

    def test_defend_edible(self):
        """Тестирование защиты съедобного растения"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.plant.defend()
            self.assertIn("Oak is being eaten", fake_out.getvalue())

    def test_defend_non_edible(self):
        """Тестирование защиты несъедобного растения"""
        non_edible_plant = Plant("Poison Ivy", "Toxicodendron", is_edible=False)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            non_edible_plant.defend()
            self.assertIn("Poison Ivy is releasing toxins to defend itself", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()