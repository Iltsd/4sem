import unittest
from unittest.mock import patch
from io import StringIO
from plant import Plant
from animal import Animal
from predator import Predator
from victim import Victim
from foodChain import FoodChain
from bioDiversity import BioDiversity
from ecoSystem import Ecosystem

class TestEcosystem(unittest.TestCase):
    def setUp(self):

        self.ecosystem = Ecosystem()
        self.lion = Predator("Lion", "Panthera leo")
        self.deer = Victim("Deer", "Cervidae")
        self.grass = Plant("Grass", "Poaceae", is_edible=True)
        self.poison_ivy = Plant("Poison Ivy", "Toxicodendron", is_edible=False)
        self.food_chain = FoodChain()

    def test_add_animal(self):

        self.ecosystem.addAnimal(self.lion)
        self.assertIn(self.lion, self.ecosystem.animals)
        self.assertIn("Lion", self.ecosystem.bioDiversity.numberOfAnimalsVariety)

    def test_add_plant(self):

        self.ecosystem.addPlant(self.grass)
        self.assertIn(self.grass, self.ecosystem.plants)
        self.assertIn("Grass", self.ecosystem.bioDiversity.numberOfPlantsVariety)

    def test_add_food_chain(self):

        self.ecosystem.addFoodChain(self.food_chain)
        self.assertIn(self.food_chain, self.ecosystem.foodChains)

    def test_remove_food_chain(self):

        self.ecosystem.addFoodChain(self.food_chain)
        self.ecosystem.removeFoodChain(1)
        self.assertNotIn(self.food_chain, self.ecosystem.foodChains)

    def test_interact_predator_eats_victim(self):

        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addAnimal(self.deer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.interact()
            self.assertIn("Lion is eating Deer", fake_out.getvalue())
            self.assertEqual(self.deer.health, 0)

    def test_interact_victim_eats_plant(self):

        self.ecosystem.addAnimal(self.deer)
        self.ecosystem.addPlant(self.grass)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.interact()
            self.assertIn("Deer is eating Grass", fake_out.getvalue())
            self.assertEqual(self.deer.energy, 110)

    def test_interact_victim_cannot_eat_poisonous_plant(self):

        self.ecosystem.addAnimal(self.deer)
        self.ecosystem.addPlant(self.poison_ivy)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.interact()
            self.assertIn("This plant is poisonous", fake_out.getvalue())
            self.assertEqual(self.deer.energy, 100)

    def test_reproduce_and_survive(self):

        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addPlant(self.grass)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.reproduceAndSurvive()
            self.assertIn("Lion is reproducing", fake_out.getvalue())
            self.assertIn("Grass is reproducing", fake_out.getvalue())
            self.assertEqual(len(self.ecosystem.animals), 2)
            self.assertEqual(len(self.ecosystem.plants), 2)

    def test_consume_resources(self):

        self.ecosystem.addAnimal(self.deer)
        self.ecosystem.addPlant(self.grass)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.consumeResources()
            self.assertIn("Deer is eating Grass", fake_out.getvalue())
            self.assertEqual(self.deer.energy, 110)

    def test_check_balance_balanced(self):

        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addAnimal(self.deer)
        self.ecosystem.addPlant(self.grass)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.checkBalance()
            self.assertIn("Ecosystem is in balance", fake_out.getvalue())

    def test_check_balance_too_many_predators(self):

        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addAnimal(self.deer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.checkBalance()
            self.assertIn("Warning: Too many predators", fake_out.getvalue())


    def test_defend_against_threats(self):

        self.ecosystem.addAnimal(self.lion)
        self.ecosystem.addAnimal(self.deer)
        self.ecosystem.addPlant(self.grass)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.defend_against_threats()
            self.assertIn("Still alive", fake_out.getvalue())
            self.assertIn("Grass is being eaten", fake_out.getvalue())

    def test_defend_against_threats_dead_animal(self):

        self.ecosystem.addAnimal(self.lion)
        self.lion.die()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ecosystem.defend_against_threats()
            self.assertNotIn("Still alive", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
