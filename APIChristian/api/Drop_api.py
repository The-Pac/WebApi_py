#link sources : 
# https://www.youtube.com/watch?v=7D_0JTeaKWg
#https://fastapi.tiangolo.com/

import http
from http.client import HTTPException

import uvicorn as uvicorn
from fastapi import Depends, FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import Croisement,Livraison,Maison,Paquet,Robot

#pour une execution sans redemarage de fastapi :
#uvicorn todo:app --reload

#connection et creation a FastAPI  
appDrop = FastAPI(title="Distribution Robotisée Opérée par la Poste",openapi_url="/0.0.0.0:8000")

appDrop.include_router(Croisement.app)
appDrop.include_router(Livraison.app)
appDrop.include_router(Maison.app)
appDrop.include_router(Paquet.app)
appDrop.include_router(Robot.app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

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
