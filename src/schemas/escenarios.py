from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VenueBase(BaseModel):
    name: str
    location: str

class VenueCreate(VenueBase):
    pass

class Venue(VenueBase):
    id: int
    class Config:
        orm_mode = True