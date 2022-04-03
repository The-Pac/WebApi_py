from pydantic import BaseModel
from os import times
import sqlite3 
import datetime

class Paquet(BaseModel):
    id_paquet : str
    addr : str
    statut_paquet : str
    date_arr : datetime.datetime.now().strftime("%d.%m.%Y_%Hh%Mm")
