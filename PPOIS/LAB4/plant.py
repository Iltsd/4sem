class Plant:
    def __init__(self, name: str, species: str, is_edible: bool):
        self._name = name
        self._species = species
        self._is_edible = is_edible
        self._health = 100
        self._is_alive = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

    @property
    def is_edible(self):
        return self._is_edible

    @is_edible.setter
    def is_edible(self, value):
        self._is_edible = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, value)
        if self._health <= 0 and self._is_alive:
            self.die()

    def grow(self):
        if self._is_alive:
            print(f"{self._name} is growing")
            self._health += 10

    def reproduce(self):
        if self._health >= 50 and self._is_alive:
            print(f"{self._name} is reproducing")
            self._health -= 50
            return Plant(f"Seedling of {self._name}", self._species, self._is_edible)
        else:
            print(f"{self._name} does not have enough health to reproduce")
            return None

    def die(self):
        if self._is_alive:
            self._health = 0
            self._is_alive = False
            print(f"{self._name} has died")

    def defend(self):
        if self._is_alive:
            if self._is_edible:
                print(f"{self._name} is being eaten")
            else:
                print(f"{self._name} is releasing toxins to defend itself")