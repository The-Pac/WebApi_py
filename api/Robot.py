from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import DB_Tables

app = APIRouter()

class Robot(BaseModel):
    statut : str
    position : str

#creation de la lecture ecriture mise à jour et suppression d'elements:
@app.get("/robots/",tags = ['Robot']) 
async def get_robots():
    try : 
        return  {DB_Tables.printRobot()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le robot avec son id d'identification
@app.get("/robots/{identifiant}",tags = ['Robot'])
async def get_robot(identifiant:str):
    try : 
        return  {DB_Tables.printRobot(identifiant=identifiant)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#ajoute un robot
@app.post("/robot",tags = ['Robot'])
async def create_robot(robot: Robot):
    return DB_Tables.addRobot(robot.statut,robot.position)
