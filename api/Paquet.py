#link use for joint database : 
# https://fastapi.tiangolo.com/advanced/dataclasses/?h=data

from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Paquet(BaseModel):
    identifiant : str
    maison : str
    date_arr : str

Paquets = []

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des paquets
@app.get("/paquets/",tags = ['Paquet']) 
async def get_paquets():
    try : 
        return  {DB_Tables.printPaquet()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le paquet avec son id d'identification
@app.get("/paquet/{identifiant}",tags = ['Paquet'])
async def get_paquet(identifiant:int):
    try : 
        return  {DB_Tables.printPaquet(identifiant=identifiant)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un paquet
@app.post("/paquet",tags = ['Paquet'])
async def create_paquet(paquet : Paquet):
    return DB_Tables.addPaquet(paquet.identifiant,paquet.maison,paquet.date_arr)
