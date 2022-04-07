#link use for joint database : 
# https://fastapi.tiangolo.com/advanced/dataclasses/?h=data

from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Paquet(BaseModel):
    maison : str
    date_arr : str

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des paquets
@app.get("/paquets/",tags = ['Paquet']) 
async def get_paquets():
    try : 
        return  {DB_Tables.printPaquet()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le paquet avec son id d'identification
@app.get("/paquets/{maison}",tags = ['Paquet'])
async def get_paquet(maison:int):
    try : 
        return  {DB_Tables.printPaquet(maison=maison)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un paquet
@app.post("/paquet",tags = ['Paquet'])
async def create_paquet(paquet : Paquet):
    return DB_Tables.addPaquet(paquet.maison,paquet.date_arr)
