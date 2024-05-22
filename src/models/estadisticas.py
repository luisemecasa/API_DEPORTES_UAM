from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..config.database import Base

class Statistic(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    points = Column(Integer)
    assists = Column(Integer)
    rebounds = Column(Integer)

    player = relationship("Player", back_populates="statistics")
    match = relationship("Match", back_populates="statistics")
