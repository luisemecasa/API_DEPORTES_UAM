from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..config.database import Base

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    
    matches = relationship("Match", back_populates="venue")
