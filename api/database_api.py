# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from fastapi import APIRouter, HTTPException

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

# get all robots
@app.get("/robots/", tags=['Robot'])
async def get_robots():
    try:
        with connectBase() as conn:
            c = conn.cursor()

            rSQL = '''SELECT * from ROBOTS '''
            c.execute(rSQL)
            rows = c.fetchall()
            for row in rows:
                yield row
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get robot with his id
@app.get("/robots/{id_robot}", tags=['Robot'])
async def get_robot(id_robot: int):
    try:
        with connectBase() as conn:
            c = conn.cursor()
            rSQL = " "
            if id_robot != '':
                rSQL = " WHERE id_robot = '" + id_robot + "' "

            rSQL = '''SELECT * from ROBOTS ''' + rSQL
            c.execute(rSQL)
            return c.fetchone()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all intersections
@app.get("/croisements/", tags=['Croisement'], response_model_exclude=id)
async def get_croisements():
    try:
        with connectBase() as conn:
            c = conn.cursor()
            rSQL = '''SELECT * from CROISEMENTS '''
            c.execute(rSQL)
            rows = c.fetchall()
            for row in rows:
                yield row
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get intersection with his id
@app.get("/croisements/{id_croisement}", tags=['Croisement'])
async def get_croisement(id_croisement: int):
    try:
        with connectBase() as conn:
            c = conn.cursor()
            if id_croisement != '':
                rSQL = " WHERE id_croisement = '" + id_croisement + "' "

            rSQL = '''SELECT * from CROISEMENTS ''' + rSQL
            c.execute(rSQL)
            return c.fetchone()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all deliveries
@app.get("/livraisons/", tags=['Livraison'])
async def get_livraisons():
    try:
        with connectBase() as conn:
            c = conn.cursor()

            rSQL = '''SELECT * from LIVRAISONS '''
            c.execute(rSQL)
            rows = c.fetchall()
            for row in rows:
                yield row
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get delivery with his id
@app.get("/livraison/{id_livraison}", tags=['Livraison'])
async def get_livraison(id_livraison: str):
    try:
        with connectBase() as conn:
            c = conn.cursor()
            if id_livraison != '':
                rSQL = " WHERE identifiant = '" + id_livraison + "' "

            rSQL = '''SELECT * from LIVRAISONS ''' + rSQL
            c.execute(rSQL)
            return c.fetchone()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all houses
@app.get("/maisons/", tags=['Maison'])
async def get_maisons():
    try:
        with connectBase() as conn:
            c = conn.cursor()

            rSQL = '''SELECT * from MAISONS '''
            c.execute(rSQL)
            rows = c.fetchall()
            for row in rows:
                yield row
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get house with his id
@app.get("/maisons/{id_maison}", tags=['Maison'])
async def get_maison(id_maison: int):
    try:
        with connectBase() as conn:
            c = conn.cursor()
            if id_maison != '':
                rSQL = " WHERE id_maison = '" + id_maison + "' "

            rSQL = '''SELECT * from MAISONS ''' + rSQL
            c.execute(rSQL)
            return c.fetchone()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get all packages
@app.get("/paquets/", tags=['Paquet'])
async def get_paquets():
    try:
        with connectBase() as conn:
            c = conn.cursor()

            rSQL = '''SELECT * from PAQUETS '''
            c.execute(rSQL)
            rows = c.fetchall()
            for row in rows:
                yield row
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


# get package with his id
@app.get("/paquets/{id_paquet}", tags=['Paquet'])
async def get_paquet(id_paquet: int):
    try:
        with connectBase() as conn:
            c = conn.cursor()
            if id_paquet != '':
                rSQL = " WHERE identifiant = '" + id_paquet + "' "

            rSQL = '''SELECT * from PAQUETS ''' + rSQL
            c.execute(rSQL)
            return c.fetchone()
    except:
        raise HTTPException(status_code=404, detail="Object not found in DataBase")


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

        # TODO changer le update
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''UPDATE LIVRAISONS SET statut = '{}' WHERE id_paquet = '{}'; '''

        c.execute(rSQL.format(statut, c.fetchone()))
        conn.commit()


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
    return True


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
        updateLivraison(c.fetchall())

    return True


def updateCroisement(identifiant, position, x, y):
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO CROISEMENTS (identifiant, position,x,y)
                        VALUES ('{}', '{}','{}', '{}') ; '''

        c.execute(rSQL.format(identifiant, position, x, y))
        conn.commit()
    return True


def updateMaison(numero, id_croisement, x, y):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = '''INSERT INTO MAISONS (numero,id_croisement,x,y)
                        VALUES ('{}','{}','{}','{}') ; '''

        c.execute(rSQL.format(numero, id_croisement, x, y))
        conn.commit()
    return True


def updateLivraison(id_paquet):
    statut = "a livrer"
    with connectBase() as conn:
        c = conn.cursor()
        # Ajouter le Nouvel object
        rSQL = '''INSERT INTO ROBOTS (id_paquet,statut)
                        VALUES ('{}', '{}') ; '''

        c.execute(rSQL.format(id_paquet, statut))
        conn.commit()
    return True


# SELECT

def selectRobot(identifiant='', nom='', statut=''):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '" + identifiant + "' "
        if nom != '':
            if rSQL == " ":
                rSQL = " WHERE nom = '" + nom + "' "
            else:
                rSQL += " and nom = '" + nom + "' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE statut = '" + statut + "' "
            else:
                rSQL += " and statut = '" + statut + "' "

        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectPaquet(identifiant='', maison='', arrivee=''):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '" + identifiant + "' "
        if maison != '':
            if rSQL == " ":
                rSQL = " WHERE maison = '" + maison + "' "
            else:
                rSQL += " and maison = '" + maison + "' "
        if arrivee != '':
            if rSQL == " ":
                rSQL = " WHERE arrivee = '" + arrivee + "' "
            else:
                rSQL += " and arrivee = '" + arrivee + "' "

        rSQL = '''SELECT * from PAQUETS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectCroisement(identifiant='', position='', x='', y=''):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '" + identifiant + "' "
        if position != '':
            if rSQL == " ":
                rSQL = " WHERE position = '" + position + "' "
            else:
                rSQL += " and position = '" + position + "' "
        if x != '':
            if rSQL == " ":
                rSQL = " WHERE x = '" + x + "' "
            else:
                rSQL += " and x = '" + x + "' "
        if y != '':
            if rSQL == " ":
                rSQL = " WHERE y = '" + y + "' "
            else:
                rSQL += " and y = '" + y + "' "

        rSQL = '''SELECT * from CROISEMENTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectMaison(identifiant='', numero='', croisement='', emplacement=''):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '" + identifiant + "' "
        if numero != '':
            if rSQL == " ":
                rSQL = " WHERE croisement = '" + croisement + "' "
            else:
                rSQL += " and croisement = '" + croisement + "' "
        if croisement != '':
            if rSQL == " ":
                rSQL = " WHERE croisement = '" + croisement + "' "
            else:
                rSQL += " and croisement = '" + croisement + "' "
        if emplacement != '':
            if rSQL == " ":
                rSQL = " WHERE emplacement = '" + emplacement + "' "
            else:
                rSQL += " and emplacement = '" + emplacement + "' "

        rSQL = '''SELECT * from MAISONS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row


def selectLivraison(identifiant='', paquet='', statut='', robot=''):
    with connectBase() as conn:
        c = conn.cursor()
        rSQL = " "
        if identifiant != '':
            rSQL = " WHERE identifiant = '" + identifiant + "' "
        if paquet != '':
            if rSQL == " ":
                rSQL = " WHERE paquet = '" + paquet + "' "
            else:
                rSQL += " and paquet = '" + paquet + "' "
        if statut != '':
            if rSQL == " ":
                rSQL = " WHERE statut = '" + statut + "' "
            else:
                rSQL += " and statut = '" + statut + "' "
        if robot != '':
            if rSQL == " ":
                rSQL = " WHERE robot = '" + robot + "' "
            else:
                rSQL += " and robot = '" + robot + "' "

        rSQL = '''SELECT * from ROBOTS ''' + rSQL
        c.execute(rSQL)
        rows = c.fetchall()
        for row in rows:
            yield row
