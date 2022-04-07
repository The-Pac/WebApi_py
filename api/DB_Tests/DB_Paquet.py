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
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        maison          INTEGER AUTOINCREMENT,
                        arrivee         TEXT,  
                        FOREIGN KEY(maison) REFERENCES MAISONS(identifiant))''')
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
def addNew(maison):
    date_Actual = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
    print(date_Actual)
    # control parameters
    msg = ''
    if type(maison) != type('A') : 
        msg += "maison  isn't correct. "
    arrivee = controlDate(date_Actual)
    if arrivee == False:
        msg += "Arrivee isn't correct. "
    if msg != '': 
        return msg
    
    with connectBase() as conn:   
        c = conn.cursor()
        #Si l'objet existe deja suppression 
        rSQL = '''DELETE FROM PAQUETS WHERE maison = '{}';'''
        c.execute(rSQL.format(maison))
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


#Affiche tous les objects en fonction des parametres saisie
def printAlls(maison='', arrivee=''):
    conn = connectBase()
    if conn:
        c = conn.cursor()
        rSQL = " "
        if maison != '':
            rSQL = " WHERE maison = '"+maison+"' "
        '''
        if arrivee != '':
            if rSQL == " ":
                rSQL = " WHERE arrivee = '"+arrivee+"' "
            else:
                rSQL += " and arrivee = '"+arrivee+"' "
        '''   
        rSQL = '''SELECT * from PAQUETS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row

def test():
    print("ajout d'un nouveau paquet")
    print("Paquet 1 :", addNew('tatu'))
    print("ajout d'un nouveau paquet")
    print("Paquet 2 :", addNew('tit'))
    print("ajout d'un nouveau paquet")
    print("Paquet 3 :", addNew('titu'))

    print("liste des objects")
    for fc in printAlls():
        print('..', fc)
    print("")

    print("liste des objects nommé 'tito'")
    for fc in printAlls(maison="tito"):
        print('..', fc)    
    print("")

if __name__ == '__main__':
    test()