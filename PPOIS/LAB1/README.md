<span style="color:purple">Модель экосистемы</span>
- # *Главные сущности*
- ## *Animal*
- ## *Predator*
- ## *Victim*
- ## *Plant*
- ## *Ecosystem*
- ## *FoodChain*
- ## *BioDiversity*
<span style="color:#59afe1"> Animal </span>
## Базовый класс для всех животных, определяющий общие свойства и поведение.
### Методы:

    eat(food) - абстрактный метод для поедания пищи (должен быть реализован в дочерних классах).

    reproduce() - размножается, если энергии достаточно.

    die() - умирает (здоровье становится 0).

    defend() - защищается, если здоровье больше 0.

<span style="color:#59af"> Predator </span>
## Класс хищника, который наследует от Animal и реализует охоту.
### Методы:

    eat(food) - хищник ест жертву (объект класса Victim).

    hunt() - хищник охотится, если у него достаточно энергии.

<span style="color:#59f"> Victim </span>
## Класс жертвы, который наследует от Animal и реализует поедание растений.
### Методы:

    eat(food) - жертва ест растение (объект класса Plant). Если растение несъедобное, выводится предупреждение.

    defend() - жертва убегает от хищников, если у нее достаточно энергии, иначе умирает.

<span style="color:#61eb34"> Plant </span>
## Класс растения, который определяет свойства и поведение растений.
### Методы:

    grow() - растение растет, увеличивая здоровье.

    reproduce() - размножается, если здоровья достаточно.

    die() - умирает (здоровье становится 0).

    defend() - защищается (выделяет токсины, если несъедобное).

<span style="color:#ebdc34"> Ecosystem </span>
## Класс экосистемы, который управляет всеми объектами (животными, растениями, цепочками).
### Методы:

    addAnimal(animal) - добавляет животное в экосистему.

      (plant) - добавляет растение в экосистему.

    addFoodChain(foodChain) - добавляет пищевую цепочку.
    
    removeFoodChain(index) - удаляет пищевую цепочку по индексу.
    
    interact() - взаимодействие между животными и растениями.
    
    reproduceAndSurvive() - размножение животных и растений.
    
    consumeResources() - потребление ресурсов (жертвы едят растения).
    
    checkBalance() - проверка баланса экосистемы.
    
    defend_against_threats() - защита от угроз (животные и растения защищаются).

<span style="color:#2a9f9f"> FoodChain </span>
## Класс пищевой цепочки, который управляет цепочками организмов.
### Методы:

    add_link(organism) - добавляет организм (животное или растение) в цепочку.
    
    remove_link(name) - удаляет организм из цепочки по имени.
    
    show_info() - выводит информацию о цепочке.

<span style="color:#2a9f9f"> BioDiversity </span>
## Класс биоразнообразия, который отслеживает разнообразие видов растений и животных.
### Методы:

    addPlantVariety(plantName) - добавляет вид растения.
    
    addAnimalVariety(animalName) - добавляет вид животного.
    
    showInfo() - выводит информацию о биоразнообразии.

# Диаграммы
## UML-диаграмма классов:
![image](https://github.com/user-attachments/assets/0c6089b0-e98c-47df-921f-c886783917b6)


## UML-диаграмма состояний:
![image](https://github.com/user-attachments/assets/0cd94e53-13cc-4933-a001-045131f72545)


### Взаимодействие классов

- `Хищники (Predator)` охотятся на жертв (Victim).

- `Жертвы (Victim)` едят растения (Plant).

- `Растения` могут быть съедобными или несъедобными, размножаются и растут.

- `Экосистема (Ecosystem)` управляет всеми объектами, проверяет баланс и взаимодействие.

- `Пищевые цепочки (FoodChain)` описывают, кто кого ест.

- `Биоразнообразие (BioDiversity)` отслеживает разнообразие видов.

Заключение
Модель экосистемы представляет собой гибкую и расширяемую систему, которая может быть использована для симуляции взаимодействий между различными организмами. Она включает в себя животных, растения, пищевые цепочки и биоразнообразие, а также управляющий класс Ecosystem, который координирует все процессы.
