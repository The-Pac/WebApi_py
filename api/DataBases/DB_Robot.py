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
                        nom       TEXT,
                        statut    TEXT
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
def addNew(id_robot,nom,statut):
    with connectBase() as conn:   
        c = conn.cursor()

        # in order to avoid replication, we control if this record already exists:
        # in this example, we try to delete directly the potential duplicate
        rSQL = '''DELETE FROM ROBOTS WHERE id_robot  = '{}'
                                           AND nom = '{}'
                                           AND statut = '{}';'''
        c.execute(rSQL.format(id_robot , nom, statut))

        #and now, insert 'new' record (really new or not) 
        rSQL = '''INSERT INTO ROBOTS (id_robot , nom, statut)
                        VALUES ('{}', '{}', '{}') ; '''

        c.execute(rSQL.format(id_robot , nom, statut))
        conn.commit()
    return True

def test():
    print("ajout d'un nouveau robot")
    print("..", addNew('titi', 'taty', 'on'))
    print("ajout d'un nouveau robot")
    print("..", addNew('tonton', 'mimo', 'on'))
    print("ajout d'un nouveau robot")
    print("..", addNew('tota', 'mimo', 'off'))
    '''
    print("liste des robots")
    for fc in printAlls():
        print('..', fc)
    print("")

    print("liste des robots nommé 'mimo'")
    for fc in printAlls(nom="mimo"):
        print('..', fc)    
    print("")
    '''
if __name__ == '__main__':
    test()

