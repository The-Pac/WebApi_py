#link sources : 
# https://www.youtube.com/watch?v=7D_0JTeaKWg

import Drop_Croisement
import Drop_Livraison
import Drop_Maison
import Drop_Paquet
import Drop_Robot

from os import times
from sqlite3 import Timestamp
from fastapi import FastAPI

#import pour lancer fastapi sans passer par le terminal 
import uvicorn
from typing import Optional
from pydantic import BaseModel


#connection et creation a FastAPI  
Drop_app = FastAPI()

@app.get("/")
async def Paquets(ident : str, addr : str, date_arr : Timestamp):
    return {"identifiant" : ident, "adresse" : addr, "date_arriver" : date_arr}

if __name__ == "_main_":
    uvicorn.run(Drop_app, host="127.0.0.1", port =8000)

