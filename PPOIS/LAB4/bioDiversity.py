
class BioDiversity:

    def __init__(self):
        self.numberOfPlantsVariety = []
        self.numberOfAnimalsVariety = []

    def addPlantVariety(self, plantName: str):
        if plantName not in self.numberOfPlantsVariety:
            self.numberOfPlantsVariety.append(plantName)
            print(f"Added new plant variety: {plantName}")
        else:
            print(f"Plant variety '{plantName}' already exists.")

    def addAnimalVariety(self, animalName: str):

        if animalName not in self.numberOfAnimalsVariety:
            self.numberOfAnimalsVariety.append(animalName)
            print(f"Added new animal variety: {animalName}")
        else:
            print(f"Animal variety '{animalName}' already exists.")

    def showInfo(self):

        print("=== Biodiversity Information ===")
        print(f"Total plant varieties: {len(self.numberOfPlantsVariety)}")
        print(f"Total animal varieties: {len(self.numberOfAnimalsVariety)}")
        print("Plant varieties:", ", ".join(self.numberOfPlantsVariety) if self.numberOfPlantsVariety else "No plant varieties added.")
        print("Animal varieties:", ", ".join(self.numberOfAnimalsVariety) if self.numberOfAnimalsVariety else "No animal varieties added.")
        print("===============================")