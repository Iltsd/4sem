import pickle
from ecoSystem import Ecosystem
from predator import Predator
from victim import Victim
from plant import Plant
from foodChain import FoodChain


class EcosystemCLI:
    def __init__(self):
        self.ecosystem = Ecosystem()
        self.SAVE_FILE = "ecosystem_state.pkl"

    def show_menu(self):
        """Отображает главное меню"""
        print("\n🌍 Ecosystem Manager")
        print("1. Добавить животное")
        print("2. Управление пищевыми цепочками")
        print("3. Добавить растение")
        print("4. Запустить симуляцию")
        print("5. Показать информацию")
        print("6. Сохранить состояние")
        print("7. Загрузить состояние")
        print("8. Выход")

    def _get_input(self, prompt, validation=None):
        while True:
            try:
                value = input(prompt)
                if validation:
                    validation(value)
                return value
            except Exception as e:
                print(f"Ошибка ввода: {str(e)}")

    def add_animal(self):
        try:
            animal_type = self._get_input(
                "Выберите тип (1-Хищник/2-Добыча): ",
                lambda x: x in ("1", "2") or _invalid("Недопустимый тип")
            )

            name = self._get_input("Введите название: ")
            species = self._get_input("Введите вид: ")

            if animal_type == "1":
                animal = Predator(name, species)
            else:
                animal = Victim(name, species)

            self.ecosystem.addAnimal(animal)
            print(f"✅ {animal.__class__.__name__} {name} добавлен!")

        except Exception as e:
            print(f"🚨 Ошибка при добавлении животного: {str(e)}")

    def manage_food_chains(self):
        try:
            print("\n🔗 Управление пищевыми цепочками")
            print("1. Добавить цепочку")
            print("2. Удалить цепочку")
            choice = self._get_input("Выберите действие: ", lambda x: x in ("1", "2"))

            if choice == "1":
                self._add_food_chain()
            else:
                self._remove_food_chain()

        except Exception as e:
            print(f"🚨 Ошибка управления цепочками: {str(e)}")

    def _add_food_chain(self):
        chain = FoodChain()
        num_links = int(self._get_input("Сколько звеньев добавить: ", lambda x: x.isdigit()))

        for i in range(num_links):
            print(f"\n🌀 Добавление звена {i + 1}/{num_links}")
            organism = self._select_organism()
            chain.add_link(organism)

        self.ecosystem.addFoodChain(chain)
        print("✅ Цепочка успешно добавлена!")

    def _remove_food_chain(self):
        if not self.ecosystem.foodChains:
            print("⚠ Нет доступных цепочек!")
            return

        print("\nСписок доступных цепочек:")
        for i, chain in enumerate(self.ecosystem.foodChains, 1):
            print(f"{i}. {chain.show_info()}")

        index = int(self._get_input("Выберите номер цепочки: ",
                                    lambda x: x.isdigit() and 1 <= int(x) <= len(self.ecosystem.foodChains))) - 1

        self.ecosystem.removeFoodChain(self.ecosystem.foodChains[index])
        print("✅ Цепочка успешно удалена!")

    def _select_organism(self):
        print("1. Животное")
        print("2. Растение")
        choice = self._get_input("Выберите тип организма: ",
                                 lambda x: x in ("1", "2") or _invalid("Недопустимый выбор"))

        if choice == "1":
            return self._select_from_list("Животные", self.ecosystem.animals)
        return self._select_from_list("Растения", self.ecosystem.plants)

    def _select_from_list(self, title, items):
        if not items:
            raise ValueError(f"Нет доступных {title.lower()}!")

        print(f"\n{title}:")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.name} ({item.species})")

        index = int(self._get_input("Выберите номер: ",
                                    lambda x: x.isdigit() and 1 <= int(x) <= len(items))) - 1

        return items[index]

    def add_plant(self):
        try:
            name = self._get_input("Введите название растения: ")
            species = self._get_input("Введите вид растения: ")
            plant = Plant(name, species, is_edible=True)
            self.ecosystem.addPlant(plant)
            print(f"🌿 Растение {name} добавлено!")
        except Exception as e:
            print(f"🚨 Ошибка при добавлении растения: {str(e)}")

    def run_simulation(self):
        try:
            print("\n🔁 Запуск симуляции...")
            self.ecosystem.interact()
            self.ecosystem.reproduceAndSurvive()
            self.ecosystem.consumeResources()
            self.ecosystem.checkBalance()
            self.ecosystem.defend_against_threats()
            print("✅ Симуляция завершена!")
        except Exception as e:
            print(f"🚨 Ошибка симуляции: {str(e)}")

    def show_info(self):
        try:
            print("\n📊 Информация о системе:")
            print(f"Всего организмов: {len(self.ecosystem.animals) + len(self.ecosystem.plants)}")
            print(f"Количество пищевых цепочек: {len(self.ecosystem.foodChains)}")

            if self.ecosystem.foodChains:
                print("\n🍴 Активные пищевые цепочки:")
                for i, chain in enumerate(self.ecosystem.foodChains, 1):
                    print(f"{i}. {chain.show_info()}")

            print("\n🌱 Биоразнообразие:")
            self.ecosystem.bioDiversity.showInfo()

        except Exception as e:
            print(f"🚨 Ошибка отображения информации: {str(e)}")

    def save_state(self):
        try:
            with open(self.SAVE_FILE, "wb") as f:
                pickle.dump(self.ecosystem, f)
            print("💾 Состояние успешно сохранено!")
        except Exception as e:
            print(f"🚨 Ошибка сохранения: {str(e)}")

    def load_state(self):
        try:
            with open(self.SAVE_FILE, "rb") as f:
                self.ecosystem = pickle.load(f)
            print("💾 Состояние успешно загружено!")
        except FileNotFoundError:
            print("⚠ Файл сохранения не найден!")
        except Exception as e:
            print(f"🚨 Ошибка загрузки: {str(e)}")

    def main(self):
        while True:
            try:
                self.show_menu()
                choice = self._get_input("Выберите действие: ",
                                         lambda x: x in map(str, range(1, 9)))

                actions = {
                    "1": self.add_animal,
                    "2": self.manage_food_chains,
                    "3": self.add_plant,
                    "4": self.run_simulation,
                    "5": self.show_info,
                    "6": self.save_state,
                    "7": self.load_state,
                    "8": lambda: print("👋 До свидания!") or exit()
                }

                actions[choice]()

            except Exception as e:
                print(f"🚨 Критическая ошибка: {str(e)}")


def _invalid(message):
    raise ValueError(message)


if __name__ == "__main__":
    cli = EcosystemCLI()
    cli.main()