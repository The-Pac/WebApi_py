#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path

databaseName = "Croisement.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE CROISEMENTS (
                        id_Croisement  INTEGER PRIMARY KEY AUTOINCREMENT,
                        x       INTERGER,
                        y       INTERGER 
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

