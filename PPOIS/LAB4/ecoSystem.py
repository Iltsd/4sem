from plant import Plant
from animal import Animal
from predator import Predator
from victim import Victim
from foodChain import FoodChain
from bioDiversity import BioDiversity

class Ecosystem:
    def __init__(self):
        self.bioDiversity = BioDiversity()
        self.animals: list[Animal] = []
        self.plants: list[Plant] = []
        self.foodChains: list[FoodChain] = []

    def addAnimal(self, animal: Animal):
        if animal.is_alive():
            self.animals.append(animal)
            self.bioDiversity.addAnimalVariety(animal.name)

    def addPlant(self, plant: Plant):
        if plant.health > 0:
            self.plants.append(plant)
            self.bioDiversity.addPlantVariety(plant.name)

    def addFoodChain(self, foodChain: FoodChain):
        self.foodChains.append(foodChain)

    def removeFoodChain(self, number: int):
        if 1 <= number <= len(self.foodChains):
            self.foodChains.pop(number - 1)

    def interact(self):
        for animal in list(self.animals):
            if not animal.is_alive() and animal in self.animals:
                self.animals.remove(animal)
                continue
            if isinstance(animal, Predator):
                for prey in list(self.animals):
                    if isinstance(prey, Victim) and prey.is_alive() and prey in self.animals:
                        animal.eat(prey)
                        if not prey.is_alive() and prey in self.animals:
                            self.animals.remove(prey)
                        break
            elif isinstance(animal, Victim) and animal.is_alive() and self.plants:
                plant = self.plants[0]
                animal.eat(plant)
                if plant.health <= 0 and plant in self.plants:
                    self.plants.remove(plant)

    def reproduceAndSurvive(self):
        new_animals = []
        new_plants = []
        for animal in list(self.animals):
            if animal.is_alive():
                baby = animal.reproduce()
                if baby:
                    new_animals.append(baby)
        for plant in list(self.plants):
            if plant.health > 0:
                seedling = plant.reproduce()
                if seedling:
                    new_plants.append(seedling)
        self.animals.extend([a for a in new_animals if a.is_alive()])
        self.plants.extend([p for p in new_plants if p.health > 0])

    def consumeResources(self):
        for animal in list(self.animals):
            if isinstance(animal, Victim) and animal.is_alive() and self.plants:
                animal.eat(self.plants[0])
                if self.plants and self.plants[0].health <= 0:
                    self.plants.remove(self.plants[0])

    def checkBalance(self):
        predator_count = sum(1 for animal in self.animals if isinstance(animal, Predator) and animal.is_alive())
        prey_count = sum(1 for animal in self.animals if isinstance(animal, Victim) and animal.is_alive())
        plant_count = sum(1 for plant in self.plants if plant.health > 0)

        if predator_count > prey_count:
            print("Warning: Too many predators, ecosystem is unbalanced")
        elif prey_count > plant_count * 2:
            print("Warning: Too many prey, ecosystem is unbalanced")
        else:
            print("Ecosystem is in balance")

    def defend_against_threats(self):
        for animal in list(self.animals):
            if animal.is_alive():
                animal.defend()
            elif animal in self.animals:
                self.animals.remove(animal)
        for plant in list(self.plants):
            if plant.health > 0:
                plant.defend()
            elif plant in self.plants:
                self.plants.remove(plant)