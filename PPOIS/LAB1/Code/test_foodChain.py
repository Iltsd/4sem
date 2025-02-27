import unittest
from unittest.mock import patch
from io import StringIO
from typing import Optional
from animal import Animal
from plant import Plant
from foodChain import FoodChain

class TestFoodChain(unittest.TestCase):
    def setUp(self):
        self.food_chain = FoodChain()
        self.animal = Animal("Lion", "Panthera leo")
        self.plant = Plant("Oak", "Quercus", is_edible=True)

    def test_initialization(self):
        self.assertEqual(self.food_chain.chain, [])

    def test_add_valid_organism(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.add_link(self.animal)
            self.food_chain.add_link(self.plant)
            self.assertEqual(self.food_chain.chain, ["Lion", "Oak"])
            self.assertIn("Added 'Lion'", fake_out.getvalue())
            self.assertIn("Added 'Oak'", fake_out.getvalue())

    def test_add_invalid_organism(self):
        with self.assertRaises(TypeError):
            self.food_chain.add_link("Invalid organism")

    def test_remove_existing_link(self):
        self.food_chain.chain = ["Lion", "Oak"]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.remove_link("Lion")
            self.assertEqual(self.food_chain.chain, ["Oak"])
            self.assertIn("Removed 'Lion'", fake_out.getvalue())

    def test_remove_non_existing_link(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.remove_link("Tiger")
            self.assertIn("not found", fake_out.getvalue())

    def test_show_info_empty(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.show_info()
            self.assertIn("Food chain is empty", fake_out.getvalue())

    def test_show_info_with_links(self):
        self.food_chain.chain = ["Grass", "Deer", "Lion"]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.show_info()
            output = fake_out.getvalue()
            self.assertIn("🔄 Food Chain:", output)
            self.assertIn("Grass → Deer → Lion → ...", output)

    def test_find_position_existing(self):
        self.food_chain.chain = ["Grass", "Deer"]
        self.assertEqual(self.food_chain.find_position("Deer"), 1)
        self.assertIsNone(self.food_chain.find_position("Lion"))

    def test_clear_chain(self):
        self.food_chain.chain = ["Grass", "Deer"]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.food_chain.clear_chain()
            self.assertEqual(self.food_chain.chain, [])
            self.assertIn("Food chain cleared", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()