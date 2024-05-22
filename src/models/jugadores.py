from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..config.database import Base
from .equipos import team_players  # Importa team_players

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    teams = relationship("Team", secondary=team_players, back_populates="players")
    captain_teams = relationship("Team", back_populates="captain", foreign_keys="[Team.captain_id]")
    statistics = relationship("Statistic", back_populates="player")

    def __repr__(self):
        return f"<Player(name={self.name}, email={self.email})>"

