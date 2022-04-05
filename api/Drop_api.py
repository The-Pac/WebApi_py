#link sources : 
# https://www.youtube.com/watch?v=7D_0JTeaKWg
#https://fastapi.tiangolo.com/

from http.client import HTTPException
from fastapi import Depends, FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from routers import Croisement,Livraison,Maison,Paquet,Robot



#pour une execution sans redemarage de fastapi :
#uvicorn todo:app --reload

#connection et creation a FastAPI  
appDrop = FastAPI(title="Distribution Robotisée Opérée par la Poste")

appDrop.include_router(Croisement.app)
appDrop.include_router(Livraison.app)
appDrop.include_router(Maison.app)
appDrop.include_router(Paquet.app)
appDrop.include_router(Robot.app)

#Les bases de donnee dont Drop_api depend
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@appDrop.get("/")
async def home():
    return {"hello" : "world"}
'''
