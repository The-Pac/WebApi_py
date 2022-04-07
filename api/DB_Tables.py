#-*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime
import json


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


def createBase():
    try:
        conn = sqlite3.connect(db_All_Table)
    except Error as e:
        return False
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        statut          TEXT,
                        position        TEXT
                        )''')
    print ("Table ROBOTS created successfully");

    c.execute('''CREATE TABLE PAQUETS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        maison          INTEGER,
                        arrivee         TEXT,  
                        FOREIGN KEY(maison) REFERENCES MAISONS(numero))''')
    print ("Table PAQUETS created successfully");

    c.execute('''CREATE TABLE CROISEMENTS (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        position        TEXT,
                        x               INTEGER,
                        y               INTERGER
                        )''')
    print ("Table CROISEMENTS created successfully");

    c.execute('''CREATE TABLE MAISONS (
                        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero                  INTEGER,
                        croisement              TEXT,
                        emplacement             TEXT,
                        FOREIGN KEY(croisement) REFERENCES CROISEMENTS(identifiant))''')
    print ("Table MAISONS created successfully");

    c.execute('''CREATE TABLE LIVRAISONS (
                        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                        paquet              INTEGER,
                        statut              TEXT,
                        robot               TEXT,
                        dateheureLivre      TEXT,
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
        conn = createBase()
        print ("Connected successfully")
        return conn
    except:
        return False

####################################################################
######## Ajouter un nouvel object en controlant ses valeurs ########
####################################################################

def addRobot(identifiant,statut= '', position=''):
    # control parameters
    msg = ''
    if statut == '': 
        statut = 'pret'
        position= 'A0T0'
    if type(identifiant)    != type('A') :              msg += "identifiant not correct. "
    if type(statut)         != type('A') :              msg += "statut 'type' isn't correct. " 
    if not statut == "en cours" and not statut == "pret" and not statut == "retour":     msg += "statut 'value' isn't correct. "
    if type(position)       != type('A') :              msg += "position 'type' isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE identifiant = '{}';'''
        c.execute(rSQL.format(identifiant))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,statut,position)
                        VALUES ('{}','{}','{}') ; '''

        c.execute(rSQL.format(identifiant, statut, position))
        conn.commit()
    return True

def addPaquet(maison):
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    # control parameters
    msg = ''
    if type(maison)             != type(0) :          msg += "maison  isn't correct. "
    arrivee = controlDate(date_Actual)
    if arrivee == False:                msg += "Arrivee isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO PAQUETS (maison,arrivee)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(maison,arrivee))
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

def addCroisement(identifiant,position='',x='',y=''):
    # control parameters
    msg = ''
    if type(identifiant)      != type('A') :          msg += "identifiant not correct. "
    if type(position)         != type('A') :          msg += "position 'type' isn't correct. " 
    if type(x)                != type(0) :            msg += "identifiant not correct. "
    if type(y)                != type(0) :            msg += "position 'type' isn't correct. " 
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM CROISEMENTS WHERE identifiant = '{}';'''
        c.execute(rSQL.format(identifiant))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO CROISEMENTS (identifiant, position,x,y)
                        VALUES ('{}', '{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant,position,x,y))
        conn.commit()
    return True

def addMaison(numero,croisement,emplacement=''):
    # control parameters
    msg = ''
    if type(numero)          != type(0):                                msg += "identifiant isn't correct. "
    if type(croisement)      != type('A') :                             msg += "croisement  isn't correct. "
    if type(emplacement)     != type('A') :                             msg += "emplacement isn't correct. " 
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM MAISONS WHERE numero = '{}' AND croisement = '{}';'''
        c.execute(rSQL.format(numero,croisement))
        #Ajouter le Nouvel object
        rSQL = '''INSERT INTO MAISONS (numero,croisement,emplacement)
                        VALUES ('{}','{}','{}') ; '''

        c.execute(rSQL.format(numero,croisement,emplacement))
        conn.commit()
    return True

def addLivraison(identifiant,paquet='',statut='',robot=''):
    # control parameters
    msg = ''
    date_Actual = ''
    if statut == '': statut = 'a livrer'
    if statut == 'livre' : 
        date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
        
    if type(identifiant)        != type('A'):               msg += "identifiant not correct. "
    if type(paquet)             != type('A') :              msg += "nom  isn't correct. "
    if type(statut)             != type('A') :              msg += "statut 'type' isn't correct. " 
    if type(robot)              != type('A'):               msg += "identifiant not correct. " 
    if not statut == "a livrer" and not statut == "en cours de livraison" and not statut == "livre" :         
        msg += "statut 'value' isn't correct. "
    dateheure = controlDate(date_Actual)
    if dateheure == False:
        msg += "Date isn't correct. "
    if msg != '': return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM ROBOTS WHERE identifiant = '{}';'''
        
        c.execute(rSQL.format(identifiant))
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

def printCroisement(identifiant='', position='', x='', y=''):
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
        if x != '':
            if rSQL == " ":
                rSQL = " WHERE x = '"+x+"' "
            else:
                rSQL += " and x = '"+x+"' "
        if y != '':
            if rSQL == " ":
                rSQL = " WHERE y = '"+y+"' "
            else:
                rSQL += " and y = '"+y+"' "
            
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
    print("Robot 1 :",  addRobot('Robi', 'en cours','A2T4'))
    print("Robot 2 :",  addRobot('Rob'))
    print("Robot 3 :",  addRobot('Ruby', 'retour','A3T1'))
    print("Robot 4 :",  addRobot('Roby', 'en cours','A4T4'))
    print("Robot 5 :",  addRobot('Rudy'))
    print("Robot 6 :",  addRobot('Ruban', 'retour','A2T4'))

    print(f"Croisement 0 :", addCroisement('A0T0','0,0',0,0))
    for i in range(4):
        for x in range(1,5):
            for y in range(1,5):
                print(f"Croisement :", addCroisement(f'A{x}T{y}',f'{x},{y}',x,y))

    for x in range(1,5):
        for y in range(1,5):
            if x == 1 and y != 1 : print("Maison 1 :", addMaison(1,f'A{x}T{y}', 'chemin'))
            if x == 2 : print("Maison 2 :", addMaison(2,f'A{x}T{y}', 'chemin'))
            if x == 3 : print("Maison 3 :", addMaison(3,f'A{x}T{y}', 'chemin'))
            if x == 4 : print("Maison 4 :", addMaison(4,f'A{x}T{y}', 'chemin'))
    
     print("Maison 4 :", addMaison(4,f'A4T4', 'chemin'))
    
    print("Paquet 1 :", addPaquet(2))
    print("Paquet 2 :", addPaquet(3))
    print("Paquet 3 :", addPaquet(3))
    print("Paquet 4 :", addPaquet(1))
    print("Paquet 5 :", addPaquet(4))
    print("Paquet 6 :", addPaquet(4))

    print("Livraison 1 :", addLivraison('2','livré', '17'))
    print("Livraison 2 :", addLivraison('65'))
    print("Livraison 3 :", addLivraison('6','en cours de livraison', '25'))
    print("Livraison 4 :", addLivraison('39','livré', '16'))
    print("Livraison 5 :", addLivraison('2'))
    print("Livraison 6 :", addLivraison('98','en cours de livraison', '28'))

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