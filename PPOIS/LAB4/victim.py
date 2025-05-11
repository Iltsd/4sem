from animal import Animal
from plant import Plant

class Victim(Animal):
    def eat(self, food):
        if self.is_alive() and isinstance(food, Plant) and food.health > 0:
            if not food.is_edible:
                print("This plant is poisonous")
                return
            print(f"{self.name} is eating {food.name}")
            self.energy += 10
            food.health -= 30  # This triggers die() in Plant if health <= 0
            if food.health <= 0:
                print(f"{food.name} has been destroyed")

    def defend(self):
        if self.is_alive():
            if self.energy > 10:
                print(f"{self.name} is running away from predators")
            else:
                self.die()