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
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        position        INTEGER 
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

#Ajouter un nouvel object en controlant ses valeurs
def addNew(identifiant,position):
    # control parameters
    msg = ''
    if type(identifiant)      != type('A') :                          msg += "identifiant not correct. "
    if type(position)         != type('A') or len(position) != 3 :    msg += "position 'type' isn't correct. " 
    #if not type(position) == "on" and not position == "off" :     msg += "position 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM CROISEMENTS WHERE identifiant = '{}'
                                           AND position = '{}';'''
        c.execute(rSQL.format(identifiant, position))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO CROISEMENTS (identifiant, position)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,position))
        conn.commit()
    return True

#Affiche tous les objects en fonction des parametres saisie
def printAlls(identifiant='', position=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        
        if position != '':
            if rSQL == " ":
                rSQL = " WHERE position = '"+position+"' "
            else:
                rSQL += " and position = '"+position+"' "
            
        rSQL = '''SELECT * from CROISEMENTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row

def test():
    print("ajout d'un nouveau robot")
    print("Croisement 1 :", addNew('3','4,5'))
    print("ajout d'un nouveau robot")
    print("Croisement 2 :", addNew('2','2,1'))
    print("ajout d'un nouveau robot")
    print("Croisement 3 :", addNew('2','4,2'))

    print("liste des objets")
    for fc in printAlls():
        print('Croisement : ', fc)
    print("")

    print("liste des objets nommés '2'")
    for fc in printAlls(identifiant='2'):
        print('Croisement : ', fc)    
    print("")

if __name__ == '__main__':
    test()
