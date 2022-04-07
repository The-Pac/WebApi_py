# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from fastapi import APIRouter

drop_db = "DROP.db"
app = APIRouter()


####################################
####### Creation des Tables ########
####################################


def createBase():
    try:
        conn = sqlite3.connect(drop_db)
    except Error as e:
        return False

    c = conn.cursor()
    c.execute('''CREATE TABLE ROBOTS (
                        id_robot        INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        statut          TEXT,
                        position        TEXT,
                        x               INTEGER ,
                        y               INTEGER
                        )''')
    print("Table ROBOTS created successfully")

    c.execute('''CREATE TABLE PAQUETS (
                        id_paquet              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant          TEXT,
                        id_maison          INTEGER,
                        date_arriver         TEXT,  
                        FOREIGN KEY(id_maison) REFERENCES MAISONS(id_maison))''')
    print("Table PAQUETS created successfully")

    c.execute('''CREATE TABLE CROISEMENTS (
                        id_croisement              INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifiant     TEXT,
                        x               INTEGER,
                        y               INTEGER 
                        )''')
    print("Table CROISEMENTS created successfully")

    c.execute('''CREATE TABLE MAISONS (
                        id_maison                     INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero                  INTEGER,
                        id_croisement              TEXT,
                        x             INTEGER ,
                        y             INTEGER,
                        FOREIGN KEY(id_croisement) REFERENCES CROISEMENTS(id_croisement))''')
    print("Table MAISONS created successfully")

    c.execute('''CREATE TABLE LIVRAISONS (
                        id_livraison                  INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_paquet              INTEGER,
                        statut              TEXT,
                        id_robot               INTEGER,
                        date_livrer      TEXT,
                        FOREIGN KEY(id_paquet) REFERENCES PAQUETS(id_paquet),
                        FOREIGN KEY(id_robot) REFERENCES ROBOTS(id_robot))''')
    conn.commit()
    print("Table LIVRAISONS created successfully")
    return conn


##################################################
####### Connections a la base de donnee ##########
##################################################

def connectBase():
    try:
        file = Path(drop_db)
        print(drop_db)
        if file.exists():
            conn = sqlite3.connect(drop_db)
            conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
            return conn
        conn = createBase()
        print("Connected successfully")
        return conn
    except:
        return False


# SELECT GET


##################################################
####### INSERT ##########
##################################################


def insertRobot(identifiant, statut):
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,statut)
                        VALUES ('{}','{}') ; '''
        c.execute(rSQL.format(identifiant, statut))
        conn.commit()


def insertLivraison(id_paquet, statut):
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO LIVRAISONS (id_paquet,statut)
                        VALUES ('{}','{}') ; '''
        c.execute(rSQL.format(id_paquet, statut))
        conn.commit()


def insertPaquet(identifiant, id_maison):
    date_arriver = str(datetime.now().strftime("%Y%m%d %H:%M:%S"))

    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO PAQUETS(id_maison,date_arriver,identifiant)
                                VALUES ('{}','{}','{}') ; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        conn.commit()

        rSQL = '''SELECT id_paquet FROM PAQUETS  WHERE id_maison = '{}' AND date_arriver = '{}' AND identifiant= '{}'; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        statut = "a livrer"


def insertCroisement(identifiant, x, y):
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO CROISEMENTS (identifiant,x,y)
                        VALUES ('{}', '{}', '{}') ; '''

        c.execute(rSQL.format(identifiant, x, y))
        conn.commit()


def insertMaison(numero, id_croisement):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO MAISONS (numero,id_croisement)
                        VALUES ('{}','{}') ; '''

        c.execute(rSQL.format(numero, id_croisement))
        conn.commit()


# UPDATE

def updateRobot(identifiant, statut, x, y):
    # control parameters
    msg = ''
    if statut == '':
        statut = 'pret'
    if not statut == "en course" and not statut == "pret":
        msg += "statut 'value' isn't correct. "
    if msg != '': return msg

    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (identifiant,statut,x,y)
                        VALUES ('{}','{}','{}','{}') ; '''
        c.execute(rSQL.format(identifiant, statut, x, y))
        conn.commit()


def updatePaquet(identifiant, id_maison):
    date_arriver = str(datetime.now().strftime("%Y%m%d %H:%M:%S"))

    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO PAQUETS(id_maison,date_arriver,identifiant)
                        VALUES ('{}','{}','{}') ; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        conn.commit()

        rSQL = '''SELECT id_paquet FROM PAQUETS  WHERE id_maison = '{}' AND date_arriver = '{}' AND identifiant= '{}'; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))

        # generate a delivery
        updateLivraison(c.fetchall())


def updateCroisement(identifiant, position, x, y):
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO CROISEMENTS (identifiant, position,x,y)
                        VALUES ('{}', '{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant, position, x, y))
        conn.commit()


def updateMaison(numero, id_croisement):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO MAISONS (numero,id_croisement)
                        VALUES ('{}','{}') ; '''

        c.execute(rSQL.format(numero, id_croisement))
        conn.commit()


def updateLivraison(id_paquet):
    statut = "a livrer"
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''UPDATE LIVRAISONS SET statut = '{}' WHERE id_paquet = '{}'; '''

        c.execute(rSQL.format(statut, id_paquet))
        conn.commit()


# SELECT

def selectRobot(id_robot):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if id_robot != '':
            rSQL = " WHERE id_robot = '" + id_robot + "' "

        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        return c.fetchone()


def selectRobots():
    with connectBase() as conn:
        c = conn.cursor()

        rSQL = '''SELECT * from ROBOTS '''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectPaquet(id_paquet):
    with connectBase() as conn:
        c = conn.cursor()
        if id_paquet != '':
            rSQL = " WHERE identifiant = '" + id_paquet + "' "

        rSQL = '''SELECT * from PAQUETS ''' + rSQL
        c.execute(rSQL)
        return c.fetchone()


def selectPaquets():
    selectPaquets()
    with connectBase() as conn:
        c = conn.cursor()

        rSQL = '''SELECT * from PAQUETS '''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectCroisement(id_croisement):
    with connectBase() as conn:
        c = conn.cursor()
        if id_croisement != '':
            rSQL = " WHERE id_croisement = '" + id_croisement + "' "

        rSQL = '''SELECT * from CROISEMENTS ''' + rSQL
        c.execute(rSQL)
        return c.fetchone()


def selectCroisements():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from CROISEMENTS '''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectMaison(id_maison):
    with connectBase() as conn:
        c = conn.cursor()
        if id_maison != '':
            rSQL = " WHERE id_maison = '" + id_maison + "' "

        rSQL = '''SELECT * from MAISONS ''' + rSQL
        c.execute(rSQL)
        return c.fetchone()


def selectMaisons():
    with connectBase() as conn:
        c = conn.cursor()

        rSQL = '''SELECT * from MAISONS '''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectLivraison(id_livraison):
    with connectBase() as conn:
        c = conn.cursor()
        if id_livraison != '':
            rSQL = " WHERE identifiant = '" + id_livraison + "' "

        rSQL = '''SELECT * from LIVRAISONS ''' + rSQL
        c.execute(rSQL)
        return c.fetchone()


def selectLivraisons():
    with connectBase() as conn:
        c = conn.cursor()

        rSQL = '''SELECT * from LIVRAISONS '''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row
