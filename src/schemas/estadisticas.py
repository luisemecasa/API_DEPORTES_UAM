from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StatisticBase(BaseModel):
    player_id: int
    match_id: int
    points: int
    assists: int
    rebounds: int

class StatisticCreate(StatisticBase):
    pass

class Statistic(StatisticBase):
    id: int
    class Config:
        from_attributes = True