from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .jugadores import Player

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    captain_id: int

class Team(TeamBase):
    id: int
    captain_id: int
    players: List[Player] = []
    class Config:
        from_attributes = True