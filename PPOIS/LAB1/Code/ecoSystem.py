from plant import Plant
from animal import Animal
from predator import Predator
from victim import Victim
from foodChain import FoodChain
from bioDiversity import BioDiversity

class Ecosystem:

    plants: list[Plant]
    animals: list[Animal]
    foodChains: list[FoodChain]
    bioDiversity: BioDiversity

    def __init__(self):
        self.bioDiversity = BioDiversity()
        self.animals: list[Animal] = []
        self.plants: list[Plant] = []
        self.foodChains: list[FoodChain] = []

    def addAnimal(self, animal: Animal):
        self.animals.append(animal)
        self.bioDiversity.addAnimalVariety(animal.name)

    def addPlant(self, plant: Plant):
        self.plants.append(plant)
        self.bioDiversity.addPlantVariety(plant.name)

    def addFoodChain(self, foodChain: FoodChain):
        self.foodChains.append(foodChain)

    def removeFoodChain(self, number: int):
        self.foodChains.pop(number-1)

    def interact(self):
        for animal in self.animals:
            if isinstance(animal, Predator):
                for prey in self.animals:
                    if isinstance(prey, Victim):
                        animal.eat(prey)
                        break
            elif isinstance(animal, Victim):
                if self.plants:
                    animal.eat(self.plants[0])

    def reproduceAndSurvive(self):
        new_animals = []
        new_plants = []
        for animal in self.animals:
            baby = animal.reproduce()
            if baby:
                new_animals.append(baby)
        for plant in self.plants:
            seedling = plant.reproduce()
            if seedling:
                new_plants.append(seedling)
        self.animals.extend(new_animals)
        self.plants.extend(new_plants)

    def consumeResources(self):
        for animal in self.animals:
            if isinstance(animal, Victim) and self.plants:
                animal.eat(self.plants[0])

    def checkBalance(self):
        predator_count = sum(1 for animal in self.animals if isinstance(animal, Predator))
        prey_count = sum(1 for animal in self.animals if isinstance(animal, Victim))
        plant_count = len(self.plants)

        if predator_count > prey_count:
            print("Warning: Too many predators, ecosystem is unbalanced")
        elif prey_count > plant_count * 2:
            print("Warning: Too many prey, ecosystem is unbalanced")
        else:
            print("Ecosystem is in balance")

    def defend_against_threats(self):
        for victims in self.animals:
            victims.defend()
        for plant in self.plants:
            plant.defend()