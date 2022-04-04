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
                        id_robot  text,
                        nom       text,
                        statut    text )
                        ''')
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
    print("st : ",statut)
    '''
    # control parameters
    msg = ''
    if type(id_robot)       != type('A') :              msg += "identifiant isn't correct. "
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    #if not statut == "on" and not statut == "off" :    msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    '''
    with connectBase() as conn:   
        c = conn.cursor()
        #controle des doublons et suppression si robot deja present dans la base
        rSQL = '''DELETE FROM ROBOT WHERE id_robot = {}
                                           AND nom = {}
                                           AND statut = {};'''
        c.execute(rSQL.format(id_robot,nom,statut))

        #le robot n'existe et il est ajouter a la base 
        rSQL = "INSERT INTO ROBOT VALUES ('{}', '{}', '{}')".format(id_robot, nom, statut)
                         #; '''
        conn.commit()
        c.execute(rSQL.format(id_robot,nom,statut))
        
    return True

#Affiche tous les robots en fonction des parametres saisie
def printAlls(id_robot='', nom='', statut=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if id_robot != '':
            rSQL = " WHERE id_robot = {"+id_robot+"} "
        if nom != '':
            if rSQL == " ":
                rSQL = " WHERE "
            else:
                rSQL += " and "
            rSQL = "nom = {"+nom+"} "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE "
            else:
                rSQL += " and "
            rSQL = "statut = {"+statut+"} "
            
        rSQL = '''SELECT * from ROBOT ''' + rSQL
        #print(rSQL)
        c.execute(rSQL)
        rows = c.fetchall()
        for _id, _id_robot,_nom,_statut in rows:
            yield  _id, _id_robot,_nom,_statut 
        conn.close()


def test():
    print("ajout d'un nouveau robot")
    print("..", addNew('titi', 'taty', 'on'))
    print("ajout d'un nouveau robot")
    print("..", addNew('tonton', 'mimo', 'on'))
    print("ajout d'un nouveau robot")
    print("..", addNew('tota', 'mimo', 'off'))

    print("liste des robots")
    for fc in printAlls():
        print('..', fc)
    print("")

    print("liste des robots nommé 'mimo'")
    for fc in printAlls(nom="mimo"):
        print('..', fc)    
    print("")

if __name__ == '__main__':
    test()

