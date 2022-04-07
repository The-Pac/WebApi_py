#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import json

databaseName = "Robot.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom             TEXT ,
                        statut          TEXT 
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
            conn.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)])
            return conn
        conn = createBase()
        print ("Connected successfully");
        return conn
    except:
        return False

#Ajouter un nouvel object en controlant ses valeurs
def addNew(nom, statut = ''):
    # control parameters
    msg = ''
    if statut == '':
        statut = 'pret'
     
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "en cours" and not statut == "pret" and not statut == "retour":     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE nom = '{}';'''
        c.execute(rSQL.format(nom))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (nom, statut)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(nom, statut))
        conn.commit()
    return True

#Affiche tous les objects en fonction des parametres saisie
def printAlls(identifiant='', nom='', statut=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if nom != '':
            if rSQL == " ":
                rSQL = " WHERE nom = '"+nom+"' "
            else:
                rSQL += " and nom = '"+nom+"' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE statut = '"+statut+"' "
            else:
                rSQL += " and statut = '"+statut+"' "
            
        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        print('rows : ',rows)
        for row in rows:
            yield row

def test():
    print("ajout d'un nouveau robot")
    print("Robot 1 :", addNew('taty', 'en cours'))
    print("ajout d'un nouveau robot")
    print("Robot 2 :", addNew('mimo'))
    print("ajout d'un nouveau robot")
    print("Robot 3 :", addNew('mimo', 'retour'))

    print("liste des objects")
    for fc in printAlls():
        print('Robot : ', fc)
    print("")

    print("liste des objects nommés 'mimo'")
    for fc in printAlls(nom='mimo'):
        print('Robot : ', fc)     
    print("")

if __name__ == '__main__':
    test()






