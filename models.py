from typing import Optional
from pydantic import BaseModel

# base model to leagues in table "times_de_basquete"
class Team(BaseModel):
    id: Optional[int] = None
    liga_id: int
    nome: str

# base model to leagues in table "ligas_de_basquete"
class League(BaseModel):
    id: Optional[int] = None
    nome: str