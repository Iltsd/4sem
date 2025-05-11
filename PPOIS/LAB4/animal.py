class Animal:
    def __init__(self, name: str, species: str):
        self._name = name
        self._species = species
        self._energy = 100
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
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = max(0, value)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, value)
        if self._health <= 0 and self._is_alive:
            self.die()

    def eat(self, food):
        raise NotImplementedError("Subclasses must implement this method")

    def reproduce(self):
        if self._energy >= 50 and self._is_alive:
            print(f"{self._name} is reproducing")
            self._energy -= 50
            return self.__class__(f"Baby {self._name}", self._species)
        else:
            print(f"{self._name} does not have enough energy to reproduce")
            return None

    def die(self):
        if self._is_alive:
            self._health = 0
            self._is_alive = False
            print(f"{self._name} has died")

    def defend(self):
        if self._is_alive:
            print("Still alive")

    def is_alive(self):
        return self._is_alive