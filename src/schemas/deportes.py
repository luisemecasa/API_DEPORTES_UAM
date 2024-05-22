from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SportBase(BaseModel):
    name: str

class SportCreate(SportBase):
    pass

class Sport(SportBase):
    id: int
    class Config:
        from_attributes = True