from pydantic import BaseModel


class Robot(BaseModel):
    identifiant: str
