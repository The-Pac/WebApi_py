#link sources : 
# https://www.youtube.com/watch?v=7D_0JTeaKWg

from fastapi import FastAPI, Form

#import pour lancer fastapi sans passer par le terminal 
import uvicorn

from typing import Optional
from pydantic import BaseModel


#connection a FastAPI et creation 
app = FastAPI()

#classe avec les parametres  necessaires au fonctionnenment 
class Essai1(BaseModel): #entree
    password : str 
    lat : float 
    lon : float
    zoom: Optional[int] = None

class Essai2(BaseModel): #sortie
    lat : float 
    lon : float
    zoom: Optional[int]= None
#les methode de communication sont get, put et delete
#test premiere api nomme hello world
#methode get 
#'@' puis nom de le methode a definir et ensuite son chemin 

@app.get("/")
async def hello_world():
    return {"hello" : "world"}


#fonction d'envois delements specifique 
@app.post("/position/", response_model= Essai2)
async def make_position(essai : Essai1):
    #db completer 
    return essai #{ "new_coord" : essai.dict()}

#pour l'execution instalation save et entrer uvicorn api:app --reload dans un termiinal puis reccuerer 
# l'adresse du serveur (dans le resultat retouner) une adresse type : "http://127.0.0.1:8000"
# et la lancer dans une page internet 

#lors d'une utilisation parametrer penser a réinitialiser fastapi en entrant dans un terminal "python3 api.py"
@app.get("/component/{component_id}") #les parametres a afficher en json
async def get_component(component_id: int):
    #instruction
    return {"component":component_id}

#reccuperer plusieurs parametres en meme temps
@app.get("/component/")
async def read_component(number: int, text:Optional[str]):
    return {"number":number , "text": text}
#instruction a lancer pour tester : http://127.0.0.1:8000/component/?number=12&text=component%20name

@app.post("/login/")
async def login(username: str = Form(...), password: str= Form(...) ):
    return {username : username}


# pour une execuction direct faire une fonction direct 
# fonction auto-documenter (plus facile a utiliser) : http://127.0.0.1:8000/docs
if __name__ == "_main_":
    uvicorn.run(app, host="127.0.0.1", port =8000)


