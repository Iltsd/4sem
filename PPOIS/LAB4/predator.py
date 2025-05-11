from animal import Animal
from victim import Victim

class Predator(Animal):
    def eat(self, food):
        if self.is_alive() and isinstance(food, Victim) and food.is_alive():
            print(f"{self.name} is eating {food.name}")
            self.energy += 20
            food.health = 0  # This triggers die() in Animal
        else:
            print(f"{self.name} cannot eat {food.name}")

    def hunt(self):
        if self.is_alive() and self.energy > 10:
            print(f"{self.name} is hunting")
        else:
            print(f"{self.name} does not have enough energy to hunt")