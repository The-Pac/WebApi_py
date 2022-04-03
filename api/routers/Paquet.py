from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = APIRouter()

class Paquet(BaseModel):
    id_paquet : str
    addr : str
    statut_paquet : str
    date_arr : str

Paquets = []

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des paquets
@app.get("/paquets/",tags = ['Paquet'],response_model=List[Paquet]) 
async def get_paquets():
    return Paquets

#Reccupere le paquet avec son id d'identification
@app.get("/paquet/{id}",tags = ['Paquet'])
async def get_paquet(id:int):
    try : 
        return Paquets[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un paquet
@app.post("/paquet/",tags = ['Paquet'])
async def create_paquet(paquet: Paquet):
    try:
        #paquet.date_arr = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")) 
        Paquets.append(paquet)
        return paquet
    except:
            raise HTTPException(status_code=404, detail="Object not found in DataBase")

#mise a jour du paquet
@app.put("/paquet/{id}",tags = ['Paquet'])
async def update_paquet(id : int , new_paquet : Paquet):
    try:
        Paquets[id] = new_paquet
        #retourne le paquet modifier
        return Paquets[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime le paquet  
@app.delete("/paquet/{id}",tags = ['Paquet'])
async def delete_paquet(id : int):
    try:
        objPaquet =Paquets[id]
        Paquets.pop(id)
        return objPaquet
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
