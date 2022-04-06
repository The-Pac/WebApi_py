from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Croisement(BaseModel):
    identifiant   : str 
    position      : int

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des croisements
@app.get("/croisements/",tags = ['Croisement'],response_model_exclude=id) 
async def get_croisements():
    try : 
        return  {DB_Tables.printCroisement()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le croisement avec son id d'identification
@app.get("/croisement/{identifiant}",tags = ['Croisement'])
async def get_croisement(identifiant: str):
    try : 
        return  {DB_Tables.printCroisement(identifiant=identifiant)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un croisement
@app.post("/croisement/",tags = ['Croisement'])
async def create_croisement(croisement: Croisement):
    return DB_Tables.addCroisement(croisement.identifiant,croisement.position)