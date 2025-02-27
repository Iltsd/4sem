from typing import Optional
from animal import Animal
from plant import Plant


class FoodChain:

    chain: list[str]

    def __init__(self):
        self.chain: list[str] = []

    def add_link(self, organism: Animal | Plant) -> None:
        if isinstance(organism, (Animal, Plant)):
            self.chain.append(organism.name)
            print(f"Added '{organism.name}' to food chain")
        else:
            raise TypeError("Only Animal or Plant can be added to the food chain")

    def remove_link(self, name: str) -> None:
        if name in self.chain:
            self.chain.remove(name)
            print(f"Removed '{name}' from food chain")
        else:
            print(f"Organism '{name}' not found in food chain")

    def show_info(self) -> None:
        if not self.chain:
            print("Food chain is empty!")
            return

        print("🔄 Food Chain:")
        print(" → ".join(self.chain) + " → ...")

    def find_position(self, name: str) -> Optional[int]:
        return self.chain.index(name) if name in self.chain else None

    def clear_chain(self) -> None:
        self.chain.clear()
        print("Food chain cleared")