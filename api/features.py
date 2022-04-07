# ajoute un robot
from fastapi import APIRouter

from api import database_api

app = APIRouter()


#############GET#############


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
