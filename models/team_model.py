from core.configs import settings
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TeamModel(settings.DBBaseModel):
    __tablename__ = "teams"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    # foreginkey
    league_id: int = Column(Integer, ForeignKey('leagues.id'))
    # league = relationship("LeagueModel", back_populates='teams', lazy='joined')

    name: str = Column(String(255))

