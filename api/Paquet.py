#link use for joint database : 
# https://fastapi.tiangolo.com/advanced/dataclasses/?h=data

from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Paquet

app = APIRouter()

class Paquet(BaseModel):
    identifiant : Optional[str]
    maison : Optional[str]
    date_arr : Optional[str]

Paquets = []

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des paquets
@app.get("/paquets/",tags = ['Paquet']) 
async def get_paquets():
    try : 
        return  {DB_Paquet.printAlls()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le paquet avec son id d'identification
@app.get("/paquet/{id}",tags = ['Paquet'])
async def get_paquet(id:int):
    try : 
        return Paquets[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un paquet
@app.post("/paquet",tags = ['Paquet'])
async def create_paquet(paquet : Paquet):
    return DB_Paquet.addNew(paquet.identifiant,paquet.maison,paquet.date_arr)
