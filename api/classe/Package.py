from pydantic import BaseModel


class Package(BaseModel):
    id_maison: int
    identifiant: str
