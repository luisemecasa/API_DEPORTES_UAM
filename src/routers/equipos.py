from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import equipos as schemas
from ..models import equipos as models
from ..config import database
from typing import List
from ..middlewares.auth import get_current_user

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, current_user: schemas.Player = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can create teams")
    db_team = models.Team(name=team.name, captain_id=team.captain_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/teams/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

@router.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, current_user: schemas.Player = Depends(get_current_user), db: Session = Depends(get_db)):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if current_user.id != db_team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can update team information")
    db_team.name = team.name
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/teams/{team_id}", response_model=schemas.Team)
def delete_team(team_id: int, current_user: schemas.Player = Depends(get_current_user), db: Session = Depends(get_db)):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if current_user.id != db_team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can delete the team")
    db.delete(db_team)
    db.commit()
    return db_team
