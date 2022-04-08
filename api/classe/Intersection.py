from pydantic import BaseModel


class Intersection(BaseModel):
    x: int
    y: int