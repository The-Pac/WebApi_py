#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime

databaseName = "Paquet.db"
 
#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE PAQUETS (
                        id_paquet       INTEGER PRIMARY KEY AUTOINCREMENT,
                        destination     TEXT NOT NULL,
                        arrivée         TEXT NOT NULL 
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

#Ajouter un nouveau robot en controlant ses valeurs
def addNew(destination,statut):
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    # control parameters
    msg = ''
    if type(destination) != type('A') : 
        msg += "destination  isn't correct. "
    if msg != '': 
        return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE destination = '{}';'''
        c.execute(rSQL.format(destination))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (destination)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(destination, statut))
        conn.commit()
    return True

#Affiche tous les robots en fonction des parametres saisie
def printAlls(id_robot='', destination='', statut=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if destination != '':
            rSQL = " WHERE id_robot = '"+destination+"' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE "
            else:
                rSQL += " and "
            rSQL = "statut = '"+statut+"' "
            
        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        #print(rSQL)
        c.execute(rSQL)
        rows = c.fetchall()
        for _id_robot,_destination,_statut in rows:
            yield  _id_robot,_destination,_statut 
        conn.close()

def test():
    print("ajout d'un nouveau paquet")
    print("..", addNew('taty', 'on'))

    print("liste des paquets")
    for fc in printAlls():
        print('..', fc)
    print("")

    print("liste des paquets nommé 'mimo'")
    for fc in printAlls(nom="mimo"):
        print('..', fc)    
    print("")

if __name__ == '__main__':
    test()