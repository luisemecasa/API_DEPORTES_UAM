from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..config.database import Base

# Tabla intermedia para la relación muchos a muchos entre equipos y jugadores
team_players = Table('team_players', Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('player_id', Integer, ForeignKey('players.id'))
)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    captain_id = Column(Integer, ForeignKey('players.id'))
    
    captain = relationship("Player", foreign_keys=[captain_id], back_populates="captain_teams")
    players = relationship("Player", secondary=team_players, back_populates="teams")
