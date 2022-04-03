import sqlite3 
from pydantic import BaseModel

class Croisement(BaseModel):
    id_croisement : str 
    x : int
    y : int
