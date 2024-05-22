from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..config.database import Base

class Jugador(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
Jugador.teams = relationship("Team", secondary="team_players", back_populates="players")
Jugador.statistics = relationship("Statistic", back_populates="player")