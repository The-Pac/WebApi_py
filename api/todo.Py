import imp
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="Todo Api", version="v1")