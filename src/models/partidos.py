from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..config.database import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    team_a_id = Column(Integer, ForeignKey('teams.id'))
    team_b_id = Column(Integer, ForeignKey('teams.id'))
    sport_id = Column(Integer, ForeignKey('sports.id'))
    score_team_a = Column(Integer)
    score_team_b = Column(Integer)

    venue = relationship("Venue", back_populates="matches")
    team_a = relationship("Team", foreign_keys=[team_a_id])
    team_b = relationship("Team", foreign_keys=[team_b_id])
    sport = relationship("Sport", back_populates="matches")
    
Match.statistics = relationship("Statistic", back_populates="match")