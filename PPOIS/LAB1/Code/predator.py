from animal import Animal
from victim import Victim

class Predator(Animal):

    def eat(self, food):
        if isinstance(food, Victim):
            print(f"{self.name} is eating {food.name}")
            self.energy += 20
            food.die()
        else:
            print(f"{self.name} cannot eat {food.name}")

    def hunt(self):
        if(self.energy > 10):
            print(f"{self.name} is hunting")
        else:
            print("not enough energy")

