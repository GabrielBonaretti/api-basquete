from typing import Optional
from pydantic import BaseModel

class Team(BaseModel):
    id: Optional[int] = None
    liga_id: int
    nome: str

class League(BaseModel):
    id: Optional[int] = None
    nome: str