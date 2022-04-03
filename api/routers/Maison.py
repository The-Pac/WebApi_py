from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = APIRouter()

class Maison(BaseModel):
    id_maison : str
    croisement : str 
    emplacement : int

Maisons = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des maisons
@app.get("/maisons/",tags = ['Maison'],response_model=List[Maison]) 
async def get_maisons():
    return Maisons

#Reccupere la maison avec son id d'identification
@app.get("/maison/{id}",tags = ['Maison'])
async def get_maison(id:int):
    try : 
        return Maisons[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute une maison
@app.post("/maison/",tags = ['Maison'])
async def create_maison(maison: Maison):
    Maisons.append(maison)
    return maison

#mise a jour de la maison
@app.put("/maison/{id}",tags = ['Maison'])
async def update_maison(id : int , new_maison : Maison):
    try:
        Maisons[id] = new_maison
        #retourne la maison modifier
        return Maisons[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime la maison  
@app.delete("/maison/{id}",tags = ['Maison'])
async def delete_maison(id : int):
    try:
        objMaison =Maisons[id]
        Maisons.pop(id)
        return objMaison
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    