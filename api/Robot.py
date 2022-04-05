from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import DB_Robot


app = APIRouter()

class Robot(BaseModel):
    identifiant : int
    nom : str
    statut : bool

Robots = []

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des robots
@app.get("/robots/",tags = ['Robot']) 
async def get_robots():
    ''' print("liste des robots")
    data : dict
    for fc in DB_Robot.printAlls():
        data += fc'''
    return Robots

#Reccupere le robot avec son id d'identification
@app.get("/robot/{id}",tags = ['Robot'])
async def get_robot(id:int):
    try : 
        return DB_Robot.printAlls(identifiant=id)
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un robot
@app.post("/robot/",tags = ['Robot'])
async def create_robot(robot: Robot):
    #Robots.append(DB_Robot.addNew(robot.identifiant,robot.nom,robot.statut))
    DB_Robot.addNew(robot.identifiant,robot.nom,robot.statut)
    return robot

'''
#A supprimer
#mise a jour du robot
@app.put("/robot/{id}",tags = ['Robot'])
async def update_robot(id : int , new_robot : Robot):
    try:
        Robots[id] = new_robot
        #retourne le robot modifier
        return Robots[id] 
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
#A supprimer
#supprime le robot  
@app.delete("/robot/{id}",tags = ['Robot'])
async def delete_robot(id : int):
    try:
        objRobot =Robots[id]
        Robots.pop(id)
        return objRobot
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
'''    
