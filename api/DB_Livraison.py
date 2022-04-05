#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import DB_Paquet

databaseName = "Livraison.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE LIVRAISONS (
                        id_Livraison    INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_paquet       INTERGER,
                        statut          TEXT,
                        robot           INTERGER,
                        dateheure       TEXT,
                        FOREIGN KEY(id_paquet) REFERENCES PAQUETS(id_paquet))''')
    conn.commit()
    print ("Table created successfully");
    return conn

#Connection a la base de donnee
def connectBase():
    try:
        file = Path(databaseName)
        if file.exists ():
            conn = sqlite3.connect(databaseName)
            return conn
        conn = createBase()
        print ("Connected successfully")
        return conn
    except:
        return False
