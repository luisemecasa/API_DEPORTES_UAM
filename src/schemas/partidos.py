from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MatchBase(BaseModel):
    date: datetime
    venue_id: int
    team_a_id: int
    team_b_id: int
    sport_id: int
    score_team_a: Optional[int]
    score_team_b: Optional[int]

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    class Config:
        orm_mode = True