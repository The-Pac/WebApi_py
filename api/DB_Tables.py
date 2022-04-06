#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime


#dbRobot = "Robot.db"
#dbPaquet = "Paquet.db"
#dbCroisement = "Croisement.db"
#dbMaison = "Maison.db"
#dbLivraison = "Livraison.db"

db_All_Table = "All_Tables.db"
#db_All_Table.

####################################
####### Creation des Tables ########
####################################


def createDBRobot():
    try:
        conn = sqlite3.connect(db_All_Table)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        nom             TEXT NOT NULL,
                        statut          TEXT NOT NULL
                        )''')
    #conn.commit()
    print ("Table ROBOTS created successfully");
    c.execute('''CREATE TABLE PAQUETS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        maison          TEXT,
                        arrivee         TEXT,  
                        FOREIGN KEY(maison) REFERENCES MAISONS(identifiant))''')
    #conn.commit()
    print ("Table PAQUETS created successfully");
    c.execute('''CREATE TABLE CROISEMENTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     INTEGER,
                        position        INTEGER 
                        )''')
    #conn.commit()
    print ("Table CROISEMENTS created successfully");
    c.execute('''CREATE TABLE MAISONS (
                        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant             TEXT,
                        numero                  INTEGER,
                        croisement              TEXT,
                        emplacement             TEXT,
                        FOREIGN KEY(croisement) REFERENCES CROISEMENTS(identifiant),
                        FOREIGN KEY(croisement) REFERENCES CROISEMENTS(identifiant))''')
    #conn.commit()
    print ("Table MAISONS created successfully");
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
    print ("Table LIVRAISONS created successfully");
    return conn

##################################################
####### Connections a la base de donnee ##########
##################################################

def connectBase():
    try:
        file = Path(db_All_Table)
        if file.exists ():
            conn = sqlite3.connect(db_All_Table)
            conn.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)])
            return conn
        conn = createDBRobot()
        
        print ("Connected successfully");
        return conn
    except:
        return False

####################################################################
######## Ajouter un nouvel object en controlant ses valeurs ########
####################################################################

def addRobot(identifiant,nom,statut):
    # control parameters
    msg = ''
    if type(identifiant)    != type('A') :              msg += "identifiant not correct. "
    if type(nom)            != type('A') :              msg += "nom  isn't correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "en cours" and not statut == "pret" and not statut == "retour":     msg += "statut 'value' isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
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
    
    with connectBase() as conn:   
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

def addMaison(identifiant,numero,croisement,emplacement):
    # control parameters
    msg = ''
    if type(identifiant)     != type('A'):                              msg += "identifiant isn't correct. "
    if type(numero)          != type(0):                                msg += "identifiant isn't correct. "
    if type(croisement)      != type('A') or len(croisement) != 4 :     msg += "croisement  isn't correct. "
    if type(emplacement)     != type('A') :                             msg += "emplacement isn't correct. " 
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM MAISONS WHERE identifiant = '{}'
                                           AND numero = '{}'
                                           AND croisement = '{}'
                                           AND emplacement = '{}';'''
        c.execute(rSQL.format(identifiant,numero,croisement,emplacement))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO MAISONS (identifiant,numero,croisement,emplacement)
                        VALUES ('{}','{}','{}','{}') ; '''

        c.execute(rSQL.format(identifiant,numero,croisement,emplacement))
        conn.commit()
    return True

def addLivraison(identifiant,paquet,statut,robot):
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

##################################################################################
########### Affiche tous les objects en fonction des parametres saisie ###########
##################################################################################

def printRobot(identifiant='', nom='', statut=''):
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
        for row in rows:
            yield row

def printPaquet(identifiant='', maison='', arrivee=''):
    conn = connectBase()
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

def printMaison(identifiant='',numero= '', croisement='', emplacement=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '"+identifiant+"' "
        if numero != '':
            if rSQL == " ":
                rSQL = " WHERE croisement = '"+croisement+"' "
            else:
                rSQL += " and croisement = '"+croisement+"' "
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

def printLivraison(identifiant='',paquet='',statut='',robot=''):
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

###################################
##########    TESTS    ############
###################################

def test():
    print("ajout d'un nouveau object")
    print("Robot 1 :", addRobot('3','taty', 'en cours'))
    print("Paquet 1 :", addPaquet('3','taty'))
    print("Croisement 1 :", addCroisement('3','4,5'))
    print("Maison 1 :", addMaison('3',2,'2,1', '4,5'))
    print("Livraison 1 :", addLivraison('3','2','2,1', '4,5'))

    print("Robot 2 :",  addRobot('5','mimo', 'pret'))
    print("Paquet 2 :", addPaquet('6','tito'))
    print("Croisement 2 :", addCroisement('2','2,1'))
    print("Maison 2 :", addMaison('5',7,'2,1', '2,1'))
    
    print("Robot 3 :",  addRobot('2','mimo', 'retour'))
    print("Paquet 3 :", addPaquet('4','tito'))
    print("Croisement 3 :", addCroisement('2','4,2'))
    print("Maison 3 :", addMaison('2',1,'3,1', '3,1'))

    print("liste des objects")
    for fc in printRobot():
        print('Robot : ', fc)
    print("")
    for fc in printPaquet():
        print('Paquet', fc)
    print("")
    for fc in printCroisement():
        print('Croisement', fc)
    print("")
    for fc in printMaison():
        print('Maison', fc)
    print("")

    print("liste des objects : 'mimo'")
    for fc in printRobot(nom='mimo'):
        print('Robot : ', fc)    
    print("")
    for fc in printPaquet(maison="tito"):
        print('Paquet', fc)    
    print("")
    for fc in printCroisement(position="2,1"):
        print('Croisement : ', fc)    
    print("")
    for fc in printMaison(croisement="2,1"):
        print('Maison :', fc)    
    print("")

if __name__ == '__main__':
    test()