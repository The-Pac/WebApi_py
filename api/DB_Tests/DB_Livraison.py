#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime
import DB_Paquet

databaseName = "Livraison.db"

#Creation de la Table
def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE LIVRAISONS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        paquet          TEXT,
                        statut          TEXT,
                        robot           TEXT,
                        dateheure       TEXT,
                        FOREIGN KEY(paquet) REFERENCES PAQUETS(identifiant),
                        FOREIGN KEY(robot) REFERENCES ROBOTS(identifiant))''')
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
        print ("Connected successfully")
        return conn
    except:
        return False

#Ajouter un nouvel object en controlant ses valeurs
def addNew(identifiant,paquet,statut,robot,dateheure):
    # control parameters
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    msg = ''
    if type(identifiant)        != type('A'):               msg += "identifiant not correct. "
    if type(paquet)             != type('A') :              msg += "nom  isn't correct. "
    if type(statut)             != type('A') :              msg += "statut 'type' isn't correct. " 
    if type(robot)              != type('A'):               msg += "identifiant not correct. " 
    if not statut == "a livrer" and not statut == "en cours de livraison" and not statut == "livré" :         
        msg += "statut 'value' isn't correct. "
    dateheure = controlDate(date_Actual)
    if dateheure == False:
        msg += "Date isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE identifiant = '{}'
                                           AND paquet = '{}'
                                           AND statut = '{}',
                                           AND robot = '{}'
                                           AND dateheure = '{}';'''
        c.execute(rSQL.format(identifiant,paquet,statut,robot,dateheure))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,paquet,statut,robot,dateheure)
                        VALUES ('{}','{}', '{}', '{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,paquet,statut,robot,dateheure))
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
def printAlls(identifiant='',paquet='',statut='',robot=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if paquet != '':
            if rSQL == " ":
                rSQL = " WHERE paquet = '"+paquet+"' "
            else:
                rSQL += " and paquet = '"+paquet+"' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE statut = '"+statut+"' "
            else:
                rSQL += " and statut = '"+statut+"' "
        if robot != '':
            if rSQL == " ":
                rSQL = " WHERE robot = '"+robot+"' "
            else:
                rSQL += " and robot = '"+robot+"' "
            
        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row

def test():
    print("ajout d'un nouveau robot")
    print("Robot 1 :", addNew(3,'taty', 'on'))
    print("ajout d'un nouveau robot")
    print("Robot 2 :", addNew(5,'mimo', 'on'))
    print("ajout d'un nouveau robot")
    print("Robot 3 :", addNew(2,'mimo', 'off'))

    print("liste des robots")
    for fc in printAlls():
        print('Robot : ', fc)
    print("")

    print("liste des robots nommés 'mimo'")
    for fc in printAlls(nom='mimo'):
        print('Robot : ', fc)    
    print("")

if __name__ == '__main__':
    test()
