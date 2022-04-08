from pydantic import BaseModel


class Delivery(BaseModel):
    id_livraison: int
    id_paquet: int
    statut: str
    id_robot: int
    date_livrer: str
