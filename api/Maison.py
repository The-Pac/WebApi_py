from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Maison(BaseModel):
    identifiant :   str
    numero :        int
    croisement :    str
    emplacement :   str


#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des maisons
@app.get("/maisons/",tags = ['Maison']) 
async def get_maisons():
    try : 
        return  {DB_Tables.printMaison()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere la maison avec son id d'identification
@app.get("/maisons/{identifiant}",tags = ['Maison'])
async def get_maison(identifiant:int):
    try : 
        return  {DB_Tables.printMaison(identifiant=identifiant)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute une maison
@app.post("/maison/",tags = ['Maison'])
async def create_maison(maison: Maison):
    return DB_Tables.addMaison(maison.identifiant,maison.numero,maison.croisement,maison.emplacement)
