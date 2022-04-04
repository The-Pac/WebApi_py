#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path

databaseName = "Paquet.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE PAQUETS (
                        id_paquet       INTERGER PRIMARY KEY,
                        destination     TEXT,
                        arrivée         TEXT 
                        )''')
    conn.commit()
    return conn
    
#Connection a la base de donnee
def connectBase():
    try:
        file = Path(databaseName)
        if file.exists ():
            conn = sqlite3.connect(databaseName)
            return conn
        conn = createBase()
        return conn
    except:
        return False