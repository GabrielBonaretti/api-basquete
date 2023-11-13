from core.configs import settings
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from models.team_model import TeamModel
from models.team_model import TeamModel


# DBbaseModel é classe declarativa do SQL Alchemy:
class LeagueModel(settings.DBBaseModel):
    __tablename__ = 'leagues'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255))

    teams = relationship(
        "TeamModel",
        cascade="all,delete-orphan",
        # back_populates="league",
        uselist=True,
        lazy="joined"
    )