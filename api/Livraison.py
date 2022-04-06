from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Livraison(BaseModel):
    identifiant :   str
    paquet :        str
    statut:         str
    robot :         str
    dateheure:      str

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des livraisons
@app.get("/livraisons/",tags = ['Livraison']) 
async def get_livraisons():
    try : 
        return  {DB_Tables.printLivraison()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere la livraison avec son id d'identification
@app.get("/livraison/{identifiant}",tags = ['Livraison'])
async def get_livraison(identifiant:int):
    try : 
        return  {DB_Tables.printLivraison(identifiant=identifiant)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute une livraison
@app.post("/livraison/",tags = ['Livraison'])
async def create_livraison(livraison: Livraison):
    return DB_Tables.addLivraison(livraison.identifiant,livraison.paquet,livraison.statut,livraison.robot,livraison.dateheure)
