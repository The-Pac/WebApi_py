from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import DB_Robot


app = APIRouter()

class Robot(BaseModel):
    identifiant : Optional[int]
    nom : Optional[str]
    statut : Optional[str]

#creation de la lecture ecriture mise à jour et suppression d'elements:
#liste des robots
#Robots = []
#get_robots():
#return Robots

@app.get("/robots/",tags = ['Robot']) 
async def get_robots():
    try : 
        return  {DB_Robot.printAlls()}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")

#Reccupere le robot avec son id d'identification
@app.get("/robots/?identifiant={i}&nom={n}&statut={s}",tags = ['Robot'])
async def get_robot(i: Optional[int], n: Optional[str], s : Optional[str]):
    try : 
        return  {DB_Robot.printAlls(i,n,s)}
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")
    
#ajoute un robot
@app.post("/robot",tags = ['Robot'])
async def create_robot(robot: Robot):
    return DB_Robot.addNew(robot.identifiant,robot.nom,robot.statut)

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
