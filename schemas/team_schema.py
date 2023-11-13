from typing import Optional
from pydantic import BaseModel as SchemaBaseModel

# COmo o sqlAlchemy yem o BaseModel dele, nao podemos confundir


class TeamSchema(SchemaBaseModel):
    id: Optional[int] = None
    league_id: int
    name: str
    
    class Config:
        from_attributes = True