from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = APIRouter()

class Livraison(BaseModel):
    id_livraison : str
    paquet : str
    statut_livraison : str
    robot : str
    dateheure : str

Livraisons = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des livraisons
@app.get("/livraisons/",tags = ['Livraison'],response_model=List[Livraison]) 
async def get_livraisons():
    return Livraisons

#Reccupere la livraison avec son id d'identification
@app.get("/livraison/{id}",tags = ['Livraison'])
async def get_livraison(id:int):
    try : 
        return Livraisons[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute une livraison
@app.post("/livraison/",tags = ['Livraison'])
async def create_livraison(livraison: Livraison):
    Livraisons.append(livraison)
    return livraison

#mise a jour de la livraison
@app.put("/livraison/{id}",tags = ['Livraison'])
async def update_livraison(id : int , new_livraison : Livraison):
    try:
        Livraisons[id] = new_livraison
        #retourne la livraison modifier
        return Livraisons[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime la livraison  
@app.delete("/livraison/{id}",tags = ['Livraison'])
async def delete_livraison(id : int):
    try:
        objLivraison =Livraisons[id]
        Livraisons.pop(id)
        return objLivraison
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
   