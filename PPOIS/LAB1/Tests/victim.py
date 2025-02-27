from animal import Animal
from plant import Plant

class Victim(Animal):

    def eat(self, food):
        if isinstance(food, Plant):
            if(food.is_edible is False):
                print("This plant is poisonous")
                return None

            print(f"{self.name} is eating {food.name}")
            self.energy += 10
        else:
            print(f"{self.name} cannot eat {food.name}")

    def defend(self):
        if(self.energy > 10):
            print(f"{self.name} is running away from predators")
        else:
            self.die()