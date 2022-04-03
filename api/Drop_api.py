#link sources : 
# https://www.youtube.com/watch?v=7D_0JTeaKWg

import Drop_Croisement
import Drop_Livraison
import Drop_Maison
import Drop_Paquet
import Drop_Robot


import sqlite3 
import datetime
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel


#pour une execution sans redemarage de fastapi :
#uvicorn todo:app --reload

#connection et creation a FastAPI  
appDrop = FastAPI(title="API DROP", version="v1")

@appDrop.get("/")
async def home():
    return {"hello" : "world"}

