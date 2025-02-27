import unittest
from unittest.mock import patch
from io import StringIO
from ecoSystem import Ecosystem
from animal import Animal
from predator import Predator
from victim import Victim
from plant import Plant
from foodChain import FoodChain
from bioDiversity import BioDiversity

class TestEcosystem(unittest.TestCase):
    def setUp(self):
        """Инициализация экосистемы перед каждым тестом"""
        self.ecosystem = Ecosystem()
        self.lion = Predator("Lion", "Panthera leo")
        self.deer = Victim("Deer", "Cervidae")
        self.grass = Plant("Grass", "Poaceae", is_edible=True)
        self.food_chain = FoodChain()

    def test_initial_state(self):
        """Тестирование начального состояния экосистемы"""
        self.assertEqual(self.ecosystem.plants, [])
        self.assertEqual(self.ecosystem.animals, [])
        self.assertEqual(self.ecosystem.foodChains, [])
        self.assertIsInstance(self.ecosystem.bioDiversity, BioDiversity)

    def test_add_animal(self):
        """Тестирование добавления животного"""
        self.ecosystem.addAnimal(self.lion)
        self.assertIn(self.lion, self.ecosystem.animals)
        self.assertIn("Lion", self.ecosystem.bioDiversity.numberOfAnimalsVariety)

    def test_add_plant(self):
        """Тестирование добавления растения"""
        self.ecosystem.addPlant(self.grass)
        self.assertIn(self.grass, self.ecosystem.plants)
        self.assertIn("Grass", self.ecosystem.bioDiversity.numberOfPlantsVariety)

    def test_add_food_chain(self):
        """Тестирование добавления пищевой цепочки"""
        self.ecosystem.addFoodChain(self.food_chain)
        self.assertIn(self.food_chain, self.ecosystem.foodChains)

    def test_remove_food_chain(self):
        """Тестирование удаления пищевой цепочки"""
        self.ecosystem.addFoodChain(self.food_chain)
        self.ecosystem.removeFoodChain(0)