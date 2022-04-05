#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path

databaseName = "Robot.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id_robot  INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom       TEXT NOT NULL,
                        statut    TEXT NOT NULL
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
        print ("Connected successfully");
        return conn
    except:
        return False

#Ajouter un nouveau robot en controlant ses valeurs
def addNew(nom,statut):
    # control parameters
    msg = ''
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "on" and not statut == "off" :     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE nom = '{}'
                                           AND statut = '{}';'''
        c.execute(rSQL.format(nom, statut))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (nom, statut)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(nom, statut))
        conn.commit()
    return True

#Affiche tous les robots en fonction des parametres saisie
def printAlls(id_robot='', nom='', statut=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if nom != '':
            rSQL = " WHERE id_robot = '"+nom+"' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE "
            else:
                rSQL += " and "
            rSQL = "statut = '"+statut+"' "
            
        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for _id_robot,_nom,_statut in rows:
            yield  _id_robot,_nom,_statut 
        conn.close()

def test():
    print("ajout d'un nouveau robot")
    print("Robot 1 :", addNew('taty', 'on'))
    print("ajout d'un nouveau robot")
    print("Robot 2 :", addNew('mimo', 'on'))
    print("ajout d'un nouveau robot")
    print("Robot 3 :", addNew('mimo', 'off'))

    print("liste des robots")
    for fc in printAlls():
        print('Robot : ', fc)
    print("")

    print("liste des robots nommés 'mimo'")
    for fc in printAlls(nom="mimo"):
        print('Robot : ', fc)    
    print("")

if __name__ == '__main__':
    test()






