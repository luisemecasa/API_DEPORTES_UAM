from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..config.database import Base



class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    captain_id = Column(Integer, ForeignKey('players.id'))
    
    captain = relationship("Player", back_populates="teams")
    players = relationship("Player", secondary="team_players", back_populates="teams")
    
    
Team.captain = relationship("Player", back_populates="teams")