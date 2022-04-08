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
    except Error:
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
        if file.exists():
            conn = sqlite3.connect(drop_db)
            conn.row_factory = sqlite3.Row
            # conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
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


def insertRobot(identifiant, statut, x, y, number_delivery):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO ROBOTS (identifiant,statut,x,y,number_delivery)
                        VALUES ('{}','{}','{}','{}','{}') ; '''
        c.execute(rSQL.format(identifiant, statut, x, y, number_delivery))
        conn.commit()


def insertLivraison(id_paquet, statut):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO LIVRAISONS (id_paquet,statut)
                        VALUES ('{}','{}') ; '''
        c.execute(rSQL.format(id_paquet, statut))
        conn.commit()


def insertPaquet(identifiant, id_maison, date_arriver):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO PAQUETS(id_maison,date_arriver,identifiant)
                                VALUES ('{}','{}','{}') ; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        conn.commit()

        rSQL = '''SELECT id_paquet FROM PAQUETS  WHERE id_maison = '{}' AND date_arriver = '{}' AND identifiant= '{}'; '''

        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        return c.fetchone()


def insertCroisement(x, y):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO CROISEMENTS (x,y)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(x, y))
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
        rSQL = '''INSERT INTO ROBOTS (identifiant,statut,x,y)
                        VALUES ('{}','{}','{}','{}') ; '''
        c.execute(rSQL.format(identifiant, statut, x, y))
        conn.commit()


def updatePaquet(identifiant, id_maison):
    date_arriver = str(datetime.now().strftime("%Y%m%d %H:%M:%S"))

    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO PAQUETS(id_maison,date_arriver,identifiant)
                        VALUES ('{}','{}','{}') ; '''
        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        conn.commit()
        rSQL = '''SELECT id_paquet FROM PAQUETS  WHERE id_maison = '{}' AND date_arriver = '{}' AND identifiant= '{}'; '''
        c.execute(rSQL.format(id_maison, date_arriver, identifiant))
        # generate a delivery
        updateLivraison(c.fetchall())


def updateCroisement(x, y):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO CROISEMENTS (x,y)
                        VALUES ('{}', '{}') ; '''
        c.execute(rSQL.format(x, y))
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
        rSQL = '''UPDATE LIVRAISONS SET statut = '{}' WHERE id_paquet = '{}'; '''
        c.execute(rSQL.format(statut, id_paquet))
        conn.commit()


# SELECT

def selectRobot(id_robot):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from ROBOTS  WHERE id_robot = '{}' ;'''
        c.execute(rSQL.format(id_robot))
        return c.fetchone()


def selectRobots():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from ROBOTS ;'''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectPaquet(id_paquet):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from PAQUETS  WHERE id_paquet = '{}' ;'''
        c.execute(rSQL.format(id_paquet))

        return c.fetchone()


def selectPaquets():
    with connectBase() as conn:
        cursor = conn.cursor()
        rSQL = '''SELECT * from PAQUETS '''
        cursor.execute(rSQL)
        rows = cursor.fetchall()
        for row in rows:
            yield [["paquet", row], ["maison", selectMaison_by_maison_id(row["id_maison"])]]


def selectCroisement(id_croisement):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from CROISEMENTS  WHERE id_croisement = '{}' ;'''
        c.execute(rSQL.format(id_croisement))
        return c.fetchone()


def selectCroisements():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from CROISEMENTS ;'''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            # yield [["croisement",row], ["maison",selectMaison_by_croisement(row["id_croisement"])]]
            yield [["croisement", row], ["maison", selectMaison_by_croisement(row["id_croisement"])]]


def selectMaison_by_croisement(id_croisement):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from MAISONS  WHERE id_croisement = '{}' ;'''
        c.execute(rSQL.format(id_croisement))
        rows = c.fetchall()
        for row in rows:
            yield row


def selectMaison_by_maison_id(id_maison: int):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from MAISONS  WHERE id_maison = '{}' ;'''
        c.execute(rSQL.format(id_maison))
        return c.fetchone()


def selectMaisons():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from MAISONS ;'''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectLivraison(id_livraison):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from LIVRAISONS  WHERE id_livraison = '{}' ;'''
        c.execute(rSQL.format(id_livraison))
        return c.fetchone()


def selectLivraisons():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from LIVRAISONS ;'''
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            paquet = selectPaquet(row["id_paquet"])
            yield [["livraison", row],
                   ["paquet", [["paquet", paquet], ["maison", selectMaison_by_maison_id(paquet["id_maison"])]]],
                   ["robot", selectRobot(row["id_robot"])]]


def select_last_Livraisons():
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT * from LIVRAISONS WHERE statut = 'a livrer' ORDER BY id_livraison ASC ;'''
        c.execute(rSQL)
        id_paquet = c.fetchone()["id_paquet"]

        rSQL = '''SELECT * from PAQUETS WHERE id_paquet = '{}';'''
        c.execute(rSQL.format(id_paquet))
        id_maison = c.fetchone()["id_maison"]

        rSQL = '''SELECT * from MAISONS WHERE id_maison = '{}';'''
        c.execute(rSQL.format(id_maison))
        house = c.fetchone()
        numero_house = house["numero"]
        id_croisement = house["id_croisement"]

        rSQL = '''SELECT * from CROISEMENTS WHERE id_croisement = '{}';'''
        c.execute(rSQL.format(id_croisement))
        croisement = c.fetchone()
        x = croisement["x"]
        y = croisement["y"]

        # return ["x", x], ["y", y], ["numero", numero_house]
        return x, y, numero_house
