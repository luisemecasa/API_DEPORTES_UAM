from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    name: str
    email: str

class PlayerCreate(PlayerBase):
    password: str

class Player(PlayerBase):
    id: int
    class Config:
        from_attributes: True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
