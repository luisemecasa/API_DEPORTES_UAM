from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    email: str

class PlayerCreate(PlayerBase):
    password: str

class Player(PlayerBase):
    id: int
    class Config:
        orm_mode = True