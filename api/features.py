# ajoute un robot
from fastapi import APIRouter, HTTPException

from api import database_api

app = APIRouter()


#############GET#############

# get all robots
@app.get("/robots/", tags=['Robot'])
async def get_robots():
    try:
        return {database_api.selectRobots()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get robot with his id
@app.get("/robots/{id_robot}", tags=['Robot'])
async def get_robot(id_robot: int):
    try:
        return {database_api.selectRobot(id_robot)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all intersections
@app.get("/croisements/", tags=['Croisement'])
async def get_croisements():
    try:
        return {database_api.selectCroisements()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get intersection with his id
@app.get("/croisements/{id_croisement}", tags=['Croisement'])
async def get_croisement(id_croisement: int):
    try:
        return {database_api.selectCroisement(id_croisement)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all deliveries
@app.get("/livraisons/", tags=['Livraison'])
async def get_livraisons():
    try:
        return {database_api.selectLivraisons()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get delivery with his id
@app.get("/livraison/{id_livraison}", tags=['Livraison'])
async def get_livraison(id_livraison: int):
    try:
        return {database_api.selectLivraison(id_livraison)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all houses
@app.get("/maisons/", tags=['Maison'])
async def get_maisons():
    try:
        return {database_api.selectMaisons()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get house with his id
@app.get("/maisons/{id_maison}", tags=['Maison'])
async def get_maison(id_maison: int):
    try:
        return {database_api.selectMaison(id_maison)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all packages
@app.get("/paquets/", tags=['Paquet'])
async def get_paquets():
    try:
        return {database_api.selectPaquets()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get package with his id
@app.get("/paquets/{id_paquet}", tags=['Paquet'])
async def get_paquet(id_paquet: int):
    try:
        return {database_api.selectPaquet(id_paquet)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


#############POST#############
@app.post("/robot/", tags=['Robot'])
async def create_robot(identifiant):
    statut = 'pret'
    database_api.insertRobot(identifiant, statut)


# ajoute un croisement
@app.post("/croisement/", tags=['Croisement'])
async def create_croisement(identifiant, x, y):
    database_api.insertCroisement(identifiant, x, y)


# TODO Add update livraison

# ajoute une maison
@app.post("/maison/", tags=['Maison'])
async def create_maison(numero, id_croisement):
    database_api.insertMaison(numero, id_croisement)


# ajoute un paquet
@app.post("/paquet/", tags=['Paquet'])
async def create_paquet(identifiant, id_maison):
    database_api.insertPaquet(identifiant, id_maison)
