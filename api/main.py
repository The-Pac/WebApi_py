import uvicorn
from fastapi import FastAPI

from api import features

app = FastAPI(title="Distribution Robotisée Opérée par la Poste")

app.include_router(features.app)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
