from typing import Optional, List
from pydantic import BaseModel as SchemaBaseModel
from schemas.team_schema import TeamSchema

# COmo o sqlAlchemy yem o BaseModel dele, nao podemos confundir
class LeagueSchema(SchemaBaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True


class LeagueRelationshipSchema(LeagueSchema):
    teams: Optional[List[TeamSchema]]