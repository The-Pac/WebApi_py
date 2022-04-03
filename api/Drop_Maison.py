import sqlite3 
import Drop_Croisement
from pydantic import BaseModel

class Maison(BaseModel):
    id_maison : str
    croisement : Drop_Croisement.id_croisement
    emplacement : int