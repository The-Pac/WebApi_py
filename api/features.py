from datetime import datetime

from fastapi import APIRouter, HTTPException

from api import database_api
from api.classe.House import House
from api.classe.Intersection import Intersection
from api.classe.Package import Package
from api.classe.Robot import Robot

app = APIRouter()


#############GET#############

# get all robots
@app.get("/robots/")
async def get_robots():
    try:
        return database_api.selectRobots()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get robot with his id
@app.get("/robots/{id_robot}")
async def get_robot(id_robot: int):
    try:
        return database_api.selectRobot(id_robot)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all intersections
@app.get("/croisements/")
async def get_croisements():
    try:
        return database_api.selectCroisements()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get intersection with his id
@app.get("/croisements/{id_croisement}")
async def get_croisement(id_croisement: int):
    try:
        return database_api.selectCroisement(id_croisement)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all deliveries
@app.get("/last_livraisons/")
async def get_last_livraisons():
    try:
        return database_api.select_last_Livraisons()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all deliveries
@app.get("/livraisons/")
async def get_livraisons():
    try:
        return database_api.selectLivraisons()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get delivery with his id
@app.get("/livraison/{id_livraison}")
async def get_livraison(id_livraison: int):
    try:
        return database_api.selectLivraison(id_livraison)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all houses
@app.get("/maisons/")
async def get_maisons():
    try:
        return database_api.selectMaisons()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get house with his id
@app.get("/maisons/{id_croisement}")
async def get_maison(id_croisement: int):
    try:
        return database_api.selectMaison_by_croisement(id_croisement)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all packages
@app.get("/paquets/")
async def get_paquets():
    try:
        return database_api.selectPaquets()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get package with his id
@app.get("/paquets/{id_paquet}")
async def get_paquet(id_paquet: int):
    try:
        return database_api.selectPaquet(id_paquet)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


#############POST#############

@app.post("/robot/")
async def create_robot(robot: Robot):
    statut = 'pret'
    x = 0
    y = 0
    number_delivery = 0
    database_api.insertRobot(robot.identifiant, statut, x, y, number_delivery)


# ajoute un croisement
@app.post("/croisement/")
async def create_croisement(intersection: Intersection):
    database_api.insertCroisement(intersection.x, intersection.y)


# ajoute une maison
@app.post("/maison/")
async def create_maison(house: House):
    database_api.insertMaison(house.numero, house.id_croisement)


# ajoute un paquet
@app.post("/paquet/")
async def create_paquet(package: Package):
    date_arriver = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    statut = "a livrer"
    id_paquet = database_api.insertPaquet(package.identifiant, package.id_maison, date_arriver)
    database_api.insertLivraison(id_paquet["id_paquet"], statut)
