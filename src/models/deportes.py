from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..config.database import Base


class Sport(Base):
    __tablename__ = "sports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    
Sport.matches = relationship("Match", back_populates="sport")