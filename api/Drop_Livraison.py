import Drop_Paquet
import Drop_Robot
import Drop_api
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3 
import datetime

class Livraison(BaseModel):
    id_livraison : str
    paquet : Drop_Paquet.id_paquet
    statut_livraison : str
    robot : Drop_Robot.id_robot
    dateheure : datetime.datetime.now().strftime("%Y%M%D %Hh:%Mm:%Ss")

Livraisons = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des livraison
@Drop_api.appDrop.get("/livraisons/",response_model=List[Livraison]) 
async def get_livraisons():
    return Livraisons

#Reccupere la livraison avec son id d'identification
@Drop_api.appDrop.get("/livraison/{id}")
async def get_livraison(id:int):
    try : 
        return Livraisons[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute une livraison
@Drop_api.appDrop.post("/livraison/")
async def create_livraison(livraison: Livraison):
    Livraisons.append(livraison)
    return livraison

#mise a jour de la livraison
@Drop_api.appDrop.put("/livraison/{id}")
async def update_livraison(id : int , new_livraison : Livraison):
    try:
        Livraisons[id] = new_livraison
        #retourne la livraison modifier
        return Livraisons[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime la livraison  
@Drop_api.appDrop.delete("/livraison/{id}")
async def delete_livraison(id : int):
    try:
        objLivraison =Livraisons[id]
        Livraisons.pop(id)
        return objLivraison
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
   