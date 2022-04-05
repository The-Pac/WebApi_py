#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import DB_Croisement

databaseName = "Maison.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE MAISONS (
                        id_maison        INTEGER PRIMARY KEY AUTOINCREMENT,
                        croisement       INTERGER,
                        emplacement      TEXT
                        )''')
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

    
    
