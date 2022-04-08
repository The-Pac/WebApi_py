from pydantic import BaseModel


class House(BaseModel):
    numero: int
    id_croisement: int
