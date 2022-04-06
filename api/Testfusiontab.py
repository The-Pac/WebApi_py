#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime

from numpy import insert


dbRobot = "Robot.db"
dbPaquet = "Paquet.db"
dbCroisement = "Croisement.db"
dbMaison = "Maison.db"
dbLivraison = "Livraison.db"

db_All_Table = "All_Tables"
#db_All_Table.

####################################
####### Creation des Tables ########
####################################

def createDBAllTable():
    try:
        conn = sqlite3.connect(db_All_Table)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE All_Table (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        nom             TEXT NOT NULL,
                        statut          TEXT NOT NULL,
                        maison          TEXT,
                        arrivee         TEXT,
                        position        INTEGER,
                        paquet          TEXT,
                        statut          TEXT,
                        robot           TEXT,
                        dateheure       TEXT
                        )''')
    conn.commit()
    print ("Table created successfully");
    return conn


def createDBRobot():
    try:
        conn = sqlite3.connect(dbRobot)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        nom             TEXT NOT NULL,
                        statut          TEXT NOT NULL
                        )''')
    conn.commit()
    print ("Table created successfully");
    return conn

def createDBPaquet():
    try:
        conn = sqlite3.connect(dbPaquet)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE PAQUETS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        maison          TEXT,
                        arrivee         TEXT,  
                        FOREIGN KEY(maison) REFERENCES MAISONS(identifiant))''')
    conn.commit()
    print ("Table created successfully");
    return conn

def createDBCroisement():
    try:
        conn = sqlite3.connect(dbCroisement)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE CROISEMENTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     INTEGER,
                        position        INTEGER 
                        )''')
    conn.commit()
    print ("Table created successfully");
    return conn

def createDBMaison():
    try:
        conn = sqlite3.connect(dbMaison)
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

def createDBLivraison():
    try:
        conn = sqlite3.connect(dbLivraison)
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
                        FOREIGN KEY(paquet) REFERENCES PAQUETS(identifiant))''')
    conn.commit()
    print ("Table created successfully");
    return conn

##################################################
####### Connections a la base de donnee ##########
##################################################

def connectBase(dbName):
    try:
        file = Path(dbName)
        if file.exists ():
            conn = sqlite3.connect(dbName)
            return conn
        if (dbName == dbRobot)          : conn = createDBRobot()
        if (dbName == dbPaquet)         : conn = createDBPaquet()
        if (dbName == dbCroisement)     : conn = createDBCroisement()
        if (dbName == dbMaison)         : conn = createDBMaison()
        if (dbName == dbLivraison)      : conn = createDBLivraison()
        if (dbName == dbLivraison)      : conn = createDBAllTable()
        
        print ("Connected successfully");
        return conn
    except:
        return False

####################################################################
######## Ajouter un nouvel object en controlant ses valeurs ########
####################################################################

def addAllTable(identifiant,nom,statut,maison,position):
    # control parameters
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    msg = ''
    if type(identifiant)    != type('A') :              msg += "identifiant not correct. "
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if type(maison)             != type('A') :          msg += "maison  isn't correct. "
    if type(position)         != type('A') or len(position) != 3 :    msg += "position 'type' isn't correct. "
    arrivee = controlDate(date_Actual)
    if not statut == "en cours" and not statut == "pret" and not statut == "retour" and arrivee == False :     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase(dbRobot) as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM All_Table WHERE identifiant = '{}'
                                           AND nom = '{}'
                                           AND statut = '{}'
                                           AND maison = '{}' 
                                           AND arrivee = '{}'
                                           AND position = '{}';
                                           '''
        c.execute(rSQL.format(identifiant,nom, statut, maison,arrivee, position))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO All_Table (identifiant,nom, statut ,maison,arrivee, position)
                        VALUES ('{}','{}', '{}', '{}', '{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,nom, statut, maison,arrivee, position))
        conn.commit()
    return True


def addRobot(identifiant,nom,statut):
    # control parameters
    msg = ''
    if type(identifiant)    != type('A') :              msg += "identifiant not correct. "
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "en cours" and not statut == "pret" and not statut == "retour":     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase(dbRobot) as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE identifiant = '{}'
                                           AND nom = '{}'
                                           AND statut = '{}';
                                           '''
        c.execute(rSQL.format(identifiant,nom, statut))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,nom, statut)
                        VALUES ('{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,nom, statut))
        conn.commit()
    return True

def addPaquet(identifiant,maison):
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    # control parameters
    msg = ''
    if type(identifiant)        != type('A') :          msg += "identifiant not correct. "
    if type(maison)             != type('A') :          msg += "maison  isn't correct. "
    arrivee = controlDate(date_Actual)
    if arrivee == False:                msg += "Arrivee isn't correct. "
    if msg != '': return msg
    
    with connectBase(dbPaquet) as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM PAQUETS WHERE identifiant = '{}' AND maison = '{}' AND arrivee = '{}';'''
        c.execute(rSQL.format(identifiant,maison,arrivee))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO PAQUETS (identifiant,maison,arrivee)
                        VALUES ('{}', '{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,maison,arrivee))
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

def addCroisement(identifiant,position):
    # control parameters
    msg = ''
    if type(identifiant)      != type('A') :                          msg += "identifiant not correct. "
    if type(position)         != type('A') or len(position) != 3 :    msg += "position 'type' isn't correct. " 
    #if not type(position) == "on" and not position == "off" :     msg += "position 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase(dbCroisement) as conn:   
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

def addMaison(identifiant,croisement,emplacement):
    # control parameters
    msg = ''
    if type(identifiant)     != type('A') :                             msg += "identifiant isn't correct. "
    if type(croisement)      != type('A') or len(croisement) != 4 :     msg += "croisement  isn't correct. "
    if type(emplacement)     != type('A') :                             msg += "emplacement isn't correct. " 
    if msg != '': return msg
    
    with connectBase(dbMaison) as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM MAISONS WHERE identifiant = '{}'
                                           AND croisement = '{}'
                                           AND emplacement = '{}';'''
        c.execute(rSQL.format(identifiant,croisement, emplacement))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO MAISONS (identifiant,croisement, emplacement)
                        VALUES ('{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,croisement, emplacement))
        conn.commit()
    return True

def addLivraison(identifiant,nom,statut):
    # control parameters
    msg = ''
    if type(identifiant)    != type('A') :              msg += "identifiant not correct. "
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "on" and not statut == "off" :     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase(dbLivraison) as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE identifiant = '{}'
                                           AND nom = '{}'
                                           AND statut = '{}';'''
        c.execute(rSQL.format(identifiant,nom, statut))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,nom, statut)
                        VALUES ('{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,nom, statut))
        conn.commit()
    return True

##################################################################################
########### Affiche tous les objects en fonction des parametres saisie ###########
##################################################################################

def printRobot(identifiant='', nom='', statut=''):
    conn = connectBase(dbRobot)
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
        for row in rows:
            yield row

def printPaquet(identifiant='', maison='', arrivee=''):
    conn = connectBase(dbPaquet)
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if maison != '':
            if rSQL == " ":
                rSQL = " WHERE maison = '"+maison+"' "
            else:
                rSQL += " and maison = '"+maison+"' "
        if arrivee != '':
            if rSQL == " ":
                rSQL = " WHERE arrivee = '"+arrivee+"' "
            else:
                rSQL += " and arrivee = '"+arrivee+"' "
            
        rSQL = '''SELECT * from PAQUETS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row

def printCroisement(identifiant='', position=''):
    conn = connectBase(dbCroisement)
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

            

###################################
##########    TESTS    ############
###################################

def test():
    print("ajout d'un nouveau object")
    print("Robot 1 :", addRobot('3','taty', 'en cours'))
    print("Paquet 1 :", addPaquet('3','taty'))

    print("Robot 2 :",  addRobot('5','mimo', 'pret'))
    print("Paquet 2 :", addPaquet('6','tito'))
    
    print("Robot 3 :",  addRobot('2','mimo', 'retour'))
    print("Paquet 3 :", addPaquet('4','tito'))

    print("liste des objects")
    for fc in printRobot():
        print('Robot : ', fc)
    print("")
    for fc in printPaquet():
        print('Paquet', fc)
    print("")

    print("liste des objects : 'mimo'")
    for fc in printRobot(nom='mimo'):
        print('Robot : ', fc)    
    print("")
    for fc in printPaquet(maison="tito"):
        print('Paquet', fc)    
    print("")
    
    
    print("ajout d'un nouveau robot")
    print("Croisement 1 :", addCroisement('3','4,5'))
    print("ajout d'un nouveau robot")
    print("Croisement 2 :", addCroisement('2','2,1'))
    print("ajout d'un nouveau robot")
    print("Croisement 3 :", addCroisement('2','4,2'))
    

    print("liste des objets")
    for fc in printCroisement():
        print('Croisement : ', fc)
    print("")

    print("liste des objets nommés '2'")
    for fc in printCroisement(identifiant='2'):
        print('Croisement : ', fc)    
    print("")
    
    
    with connectBase(dbRobot) as conn:   
        c = conn.cursor()
        rSQL = '''ATTACH 'Robot.db' as rob ;  '''

        c.execute(rSQL)
        rSQL = '''SELECT * from rob.ROBOTS; '''
        rows = c.execute(rSQL)
        conn.commit()
        print("ATTACH Robi")
        for row in rows:
            print( row)
            
    with connectBase(dbPaquet) as conn:   
        c = conn.cursor()
        rSQL = '''ATTACH 'Paquet.db' as paq ;  '''

        c.execute(rSQL)
        rSQL = '''SELECT * from paq.PAQUETS; '''
        rows = c.execute(rSQL)
        conn.commit()
        print("ATTACH Paquet")
        for row in rows:
            print( row)
        conn = sqlite3.connect
        c = conn.cursor()
        rSQL = '''SELECT * from rob.ROBOTS as r , paq.PAQUETS as m where r.identifiant=m.identifiant;  '''
        rows = c.execute(rSQL)
        conn.commit()
        print("ATTACH Robot U Paquet")
        for row in rows:
            print( row)
        
    
    
    
    


    
    

if __name__ == '__main__':
    test()