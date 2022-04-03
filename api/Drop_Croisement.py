import Drop_api
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3 

class Croisement(BaseModel):
    id_croisement : str 
    x : int
    y : int

Croisements = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des croisements
@Drop_api.appDrop.get("/croisements/",response_model=List[Croisement]) 
async def get_croisements():
    return Croisements

#Reccupere le croisement avec son id d'identification
@Drop_api.appDrop.get("/croisement/{id}")
async def get_croisement(id:int):
    try : 
        return Croisements[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un croisement
@Drop_api.appDrop.post("/croisement/")
async def create_croisement(croisement: Croisement):
    Croisements.append(croisement)
    return croisement

#mise a jour du croisement
@Drop_api.appDrop.put("/croisement/{id}")
async def update_croisement(id : int , new_croisement : Croisement):
    try:
        Croisements[id] = new_croisement
        #retourne le croisement modifier
        return Croisements[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime le croisement  
@Drop_api.appDrop.delete("/livraison/{id}")
async def delete_croisement(id : int):
    try:
        objCroisement =Croisements[id]
        Croisements.pop(id)
        return objCroisement
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    