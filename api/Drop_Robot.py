import sqlite3 
from pydantic import BaseModel

class Robot(BaseModel):
    id_robot : str
    nom_robot : str
    statut_robot : bool

