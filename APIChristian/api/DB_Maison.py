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
                        id        INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant      INTEGER,
                        numero
                        croisement       INTEGER,
                        emplacement      TEXT,
                        FOREIGN KEY(croisement) REFERENCES CROISEMENTS(identifiant),
                        FOREIGN KEY(croisement) REFERENCES CROISEMENTS(identifiant))''')
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
def addNew(identifiant,croisement,emplacement):
    # control parameters
    msg = ''
    if type(identifiant)     != type(0) or\
       identifiant < 0:                                                 msg += "identifiant isn't correct. "
    if type(croisement)      != type('A') or len(croisement) != 4 :     msg += "croisement  isn't correct. "
    if type(emplacement)     != type('A') :                             msg += "emplacement isn't correct. " 
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO MAISONS (identifiant,croisement, emplacement)
                        VALUES ('{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,croisement, emplacement))
        conn.commit()
    return True

#Affiche tous les objects en fonction des parametres saisie
def printAlls(identifiant='', croisement='', emplacement=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if croisement != '':
            if rSQL == " ":
                rSQL = " WHERE croisement = '"+croisement+"' "
            else:
                rSQL += " and croisement = '"+croisement+"' "
        if emplacement != '':
            if rSQL == " ":
                rSQL = " WHERE emplacement = '"+emplacement+"' "
            else:
                rSQL += " and emplacement = '"+emplacement+"' "
            
        rSQL = '''SELECT * from MAISONS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row

def test():
    print("ajout d'un nouveau maison")
    print("Maison 1 :", addNew(3,'taty', 'on'))
    print("ajout d'un nouveau maison")
    print("Maison 2 :", addNew(5,'mimo', 'on'))
    print("ajout d'un nouveau maison")
    print("Maison 3 :", addNew(2,'mimo', 'off'))

    print("liste des objects")
    for fc in printAlls():
        print('Maison : ', fc)
    print("")

    print("liste des robots nommés 'mimo'")
    for fc in printAlls(croisement='mimo'):
        print('Maison : ', fc)    
    print("")

if __name__ == '__main__':
    test()    
    
