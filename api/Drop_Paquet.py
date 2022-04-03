import Drop_api
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3 
import datetime

class Paquet(BaseModel):
    id_paquet : str
    addr : str
    statut_paquet : str
    date_arr : datetime.datetime.now().strftime("%Y%M%D %Hh:%Mm:%Ss")

Paquets = []

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des paquets
@Drop_api.appDrop.get("/paquets/",response_model=List[Paquets]) 
async def get_paquets():
    return Paquets

#Reccupere le paquet avec son id d'identification
@Drop_api.appDrop.get("/paquet/{id}")
async def get_paquet(id:int):
    try : 
        return Paquets[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un paquet
@Drop_api.appDrop.post("/paquet/")
async def create_paquet(paquet: Paquet):
    Paquets.append(paquet)
    return paquet

#mise a jour du paquet
@Drop_api.appDrop.put("/paquet/{id}")
async def update_paquet(id : int , new_paquet : Paquet):
    try:
        Paquets[id] = new_paquet
        #retourne le paquet modifier
        return Paquets[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime le paquet  
@Drop_api.appDrop.delete("/paquet/{id}")
async def delete_paquet(id : int):
    try:
        objPaquet =Paquets[id]
        Paquets.pop(id)
        return objPaquet
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
