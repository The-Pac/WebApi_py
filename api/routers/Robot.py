from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = APIRouter()

class Robot(BaseModel):
    id_robot : int
    nom_robot : str
    statut_robot : bool

Robots = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des robots
@app.get("/robots/",tags = ['Robot'],response_model=List[Robot]) 
async def get_robots():
    return Robots

#Reccupere le robot avec son id d'identification
@app.get("/robot/{id}",tags = ['Robot'])
async def get_robot(id:int):
    try : 
        return Robots[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un robot
@app.post("/robot/",tags = ['Robot'])
async def create_robot(robot: Robot):
    Robots.append(robot)
    return robot

#mise a jour du robot
@app.put("/robot/{id}",tags = ['Robot'])
async def update_robot(id : int , new_robot : Robot):
    try:
        Robots[id] = new_robot
        #retourne le robot modifier
        return Robots[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime le robot  
@app.delete("/robot/{id}",tags = ['Robot'])
async def delete_robot(id : int):
    try:
        objRobot =Robots[id]
        Robots.pop(id)
        return objRobot
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
