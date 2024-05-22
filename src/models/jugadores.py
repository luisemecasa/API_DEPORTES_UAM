from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..config import database

class Player(database.Base):
    __tablename__ = "player"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    teams = relationship("Team", secondary="team_players", back_populates="players")
    statistics = relationship("Statistic", back_populates="player")

    def __repr__(self):
        return f"<Player(name={self.name}, email={self.email})>"
