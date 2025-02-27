class Plant:

    name: str
    species: str
    isEdible: bool

    def __init__(self, name: str, species: str, is_edible: bool):
        self.name = name
        self.species = species
        self.is_edible = is_edible
        self.health = 100

    def grow(self):
        print(f"{self.name} is growing")
        self.health += 10

    def reproduce(self):
        if self.health >= 50:
            print(f"{self.name} is reproducing")
            self.health -= 50
            return Plant(f"Seedling of {self.name}", self.species, self.is_edible)
        else:
            print(f"{self.name} does not have enough health to reproduce")
            return None

    def die(self):
        self.health = 0
        print(f"{self.name} has died")

    def defend(self):
        if self.is_edible:
            print(f"{self.name} is being eaten")
        else:
            print(f"{self.name} is releasing toxins to defend itself")