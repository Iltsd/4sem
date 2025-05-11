from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import jsonpickle
from ecoSystem import Ecosystem
from predator import Predator
from victim import Victim
from plant import Plant
from foodChain import FoodChain

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Загрузка экосистемы
ecosystem = None
try:
    with open("ecosystem.json", "r") as f:
        content = f.read()
        if content.strip():
            ecosystem = jsonpickle.decode(content)
        else:
            ecosystem = Ecosystem()
except (FileNotFoundError, jsonpickle.JsonPickleException):
    ecosystem = Ecosystem()

# Сохранение экосистемы
def save_ecosystem():
    with open("ecosystem.json", "w") as f:
        f.write(jsonpickle.encode(ecosystem))

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "animals": ecosystem.animals, "plants": ecosystem.plants}
    )

# Форма для добавления животного
@app.get("/add_animal", response_class=HTMLResponse)
async def add_animal_form(request: Request):
    return templates.TemplateResponse("add_animal.html", {"request": request})

@app.post("/add_animal", response_class=HTMLResponse)
async def add_animal(
    request: Request,
    name: str = Form(...),
    species: str = Form(...),
    type: str = Form(...)
):
    if type == "predator":
        animal = Predator(name, species)
    elif type == "victim":
        animal = Victim(name, species)
    else:
        return templates.TemplateResponse(
            "add_animal.html",
            {"request": request, "message": "Неверный тип животного"}
        )
    ecosystem.addAnimal(animal)
    save_ecosystem()
    return templates.TemplateResponse(
        "add_animal.html",
        {"request": request, "message": f"Животное {name} добавлено"}
    )

# Форма для добавления растения
@app.get("/add_plant", response_class=HTMLResponse)
async def add_plant_form(request: Request):
    return templates.TemplateResponse("add_plant.html", {"request": request})

@app.post("/add_plant", response_class=HTMLResponse)
async def add_plant(
    request: Request,
    name: str = Form(...),
    species: str = Form(...),
    is_edible: bool = Form(default=False)
):
    plant = Plant(name, species, is_edible)
    ecosystem.addPlant(plant)
    save_ecosystem()
    return templates.TemplateResponse(
        "add_plant.html",
        {"request": request, "message": f"Растение {name} добавлено"}
    )

# Удаление животного
@app.get("/remove_animal/{name}", response_class=HTMLResponse)
async def remove_animal(request: Request, name: str):
    for animal in list(ecosystem.animals):
        if animal.name == name:
            ecosystem.animals.remove(animal)
            break
    save_ecosystem()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": f"Животное {name} удалено"
        }
    )

# Удаление растения
@app.get("/remove_plant/{name}", response_class=HTMLResponse)
async def remove_plant(request: Request, name: str):
    for plant in list(ecosystem.plants):
        if plant.name == name:
            ecosystem.plants.remove(plant)
            break
    save_ecosystem()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": f"Растение {name} удалено"
        }
    )

# Запуск взаимодействия
@app.get("/interact", response_class=HTMLResponse)
async def interact(request: Request):
    ecosystem.interact()
    save_ecosystem()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": "Взаимодействие выполнено"
        }
    )

# Запуск размножения
@app.get("/reproduce", response_class=HTMLResponse)
async def reproduce(request: Request):
    ecosystem.reproduceAndSurvive()
    save_ecosystem()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": "Размножение выполнено"
        }
    )

# Потребление ресурсов
@app.get("/consume", response_class=HTMLResponse)
async def consume(request: Request):
    ecosystem.consumeResources()
    save_ecosystem()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": "Потребление ресурсов выполнено"
        }
    )

# Проверка баланса
@app.get("/check_balance", response_class=HTMLResponse)
async def check_balance(request: Request):
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        ecosystem.checkBalance()
    balance_message = f.getvalue().strip()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "animals": ecosystem.animals,
            "plants": ecosystem.plants,
            "message": f"Баланс: {balance_message}"
        }
    )

# Управление пищевой цепочкой
@app.get("/food_chain", response_class=HTMLResponse)
async def food_chain(request: Request):
    return templates.TemplateResponse(
        "food_chain.html",
        {
            "request": request,
            "food_chains": ecosystem.foodChains
        }
    )

@app.post("/add_food_chain", response_class=HTMLResponse)
async def add_food_chain(request: Request, organism_name: str = Form(...)):
    food_chain = FoodChain()
    found = False
    for organism in ecosystem.animals + ecosystem.plants:
        if organism.name == organism_name:
            food_chain.add_link(organism)
            ecosystem.addFoodChain(food_chain)
            save_ecosystem()
            found = True
            break
    message = f"Организм {organism_name} добавлен в пищевую цепочку" if found else f"Организм {organism_name} не найден"
    return templates.TemplateResponse(
        "food_chain.html",
        {
            "request": request,
            "food_chains": ecosystem.foodChains,
            "message": message
        }
    )

# Информация о биоразнообразии
@app.get("/biodiversity", response_class=HTMLResponse)
async def biodiversity(request: Request):
    biodiversity_info = {
        "plant_varieties": ecosystem.bioDiversity.numberOfPlantsVariety,
        "animal_varieties": ecosystem.bioDiversity.numberOfAnimalsVariety
    }
    return templates.TemplateResponse(
        "biodiversity.html",
        {"request": request, "biodiversity": biodiversity_info}
    )