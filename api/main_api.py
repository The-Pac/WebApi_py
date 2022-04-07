from fastapi import FastAPI

from api import database_api

# connection et creation a FastAPI
appDrop = FastAPI(title="Distribution Robotisée Opérée par la Poste")

appDrop.include_router(database_api.app)
