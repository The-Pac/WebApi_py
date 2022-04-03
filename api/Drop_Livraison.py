import Drop_Paquet
import Drop_Robot
from pydantic import BaseModel
import sqlite3 
import datetime

class livraison(BaseModel):
    id_Livraison : str
    paquet : Drop_Paquet.id_paquet
    statut_livraison : str
    robot : Drop_Robot.id_robot
    dateheure : datetime.datetime.now().strftime("%d.%m.%Y_%Hh%Mm")