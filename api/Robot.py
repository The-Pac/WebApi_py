#import Drop_api
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3 

app = FastAPI()

class Robot(BaseModel):
    id_robot : str
    nom_robot : str
    statut_robot : bool

Robots = [

]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des robots
@app.get("/robots/",tags = ['Croisement'],response_model=List[Robot]) 
async def get_robots():
    return Robots

#Reccupere le robot avec son id d'identification
@app.get("/robot/{id}",tags = ['Croisement'])
async def get_robot(id:int):
    try : 
        return Robots[id]
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un robot
@app.post("/robot/",tags = ['Croisement'])
async def create_robot(robot: Robot):
    Robots.append(robot)
    return robot

#mise a jour du robot
@app.put("/robot/{id}",tags = ['Croisement'])
async def update_robot(id : int , new_robot : Robot):
    try:
        Robots[id] = new_robot
        #retourne le robot modifier
        return Robots[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#supprime le robot  
@app.delete("/robot/{id}",tags = ['Croisement'])
async def delete_robot(id : int):
    try:
        objRobot =Robots[id]
        Robots.pop(id)
        return objRobot
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
