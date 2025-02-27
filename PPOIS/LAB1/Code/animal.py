class Animal:
    name: str
    species: str
    energy = 100
    health = 100

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.energy = 100
        self.health = 100

    def eat(self, food):
        raise NotImplementedError("Subclasses must implement this method")

    def reproduce(self):
        if self.energy >= 50:
            print(f"{self.name} is reproducing")
            self.energy -= 50
            return self.__class__(f"Baby {self.name}", self.species)
        else:
            print(f"{self.name} does not have enough energy to reproduce")
            return None

    def die(self):
        self.health = 0
        print(f"{self.name} has died")

    def defend(self):
        if(self.health > 0): print("Still alive")