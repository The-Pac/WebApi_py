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
                        id              INTEGER PRIMARY KEY ,
                        identifiant     INTEGER,
                        destination     TEXT NOT NULL,
                        arrivee         TEXT  
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
def addNew(identifiant,destination):
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    # control parameters
    msg = ''
    if type(identifiant)       != type(0) or\
       identifiant < 0:                                    msg += "identifiant not correct. "
    if type(destination) != type('A') : 
        msg += "destination  isn't correct. "
    arrivee = controlDate(date_Actual)
    if arrivee == False:
        msg += "Arrivee isn't correct. "
    if msg != '': 
        return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM PAQUETS WHERE identifiant = '{}' AND destination = '{}' AND arrivee = '{}';'''
        c.execute(rSQL.format(identifiant,destination,arrivee))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO PAQUETS (identifiant,destination,arrivee)
                        VALUES ('{}', '{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,destination,arrivee))
        conn.commit()
    return True

def controlDate(dateActual):
    # controle du format =    YYYYMMDD HH:MM:SS
    ymd,hms = dateActual.split(" ")
    ymd = addDays(ymd,0)
    if not ymd: return False

    h,m,s = [ int(x) for x in hms.split(":") ]
    if h > 24 or h <0: return False
    if m > 59 or m <0: return False
    if s > 59 or s <0: return False
    
    return ymd+" "+hms
    

def addDays(dateActual,diff):
    y,m,d = dateActual[0:4],dateActual[4:6],dateActual[6:]
    try:
        d = datetime.datetime(int(y),int(m),int(d)) + datetime.timedelta(days=diff)
        d = str(d).split(" ")[0]
    except:
        return False

    if '-' in dateActual:
        return d
    else:
        return d.replace('-','')


#Affiche tous les objects en fonction des parametres saisie
def printAlls(identifiant='', destination='', arrivee=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if destination != '':
            if rSQL == " ":
                rSQL = " WHERE destination = '"+destination+"' "
            else:
                rSQL += " and destination = '"+destination+"' "
        if arrivee != '':
            if rSQL == " ":
                rSQL = " WHERE arrivee = '"+arrivee+"' "
            else:
                rSQL += " and arrivee = '"+arrivee+"' "
            
        rSQL = '''SELECT * from PAQUETS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for _id,_identifiant,_destination,_arrivee in rows:
            yield  _id,_identifiant,_destination,_arrivee 
        conn.close()

def test():
    print("ajout d'un nouveau paquet")
    print("Paquet 1 :", addNew(3,'taty'))
    print("ajout d'un nouveau paquet")
    print("Paquet 2 :", addNew(6,'tito'))
    print("ajout d'un nouveau paquet")
    print("Paquet 3 :", addNew(4,'tito'))

    print("liste des paquets")
    for fc in printAlls():
        print('..', fc)
    print("")

    print("liste des paquets nommé 'tito'")
    for fc in printAlls(destination="tito"):
        print('..', fc)    
    print("")

if __name__ == '__main__':
    test()