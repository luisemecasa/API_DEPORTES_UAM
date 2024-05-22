from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import equipos as schemas
from ..models import equipos as models
from ..config import database
from ..middlewares import auth
from typing import List

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new team
@router.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, current_user: schemas.Player = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is the captain (only captain can create teams)
    if current_user.id != team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can create teams")
    db_team = models.Team(name=team.name, captain_id=team.captain_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

# Get all teams
@router.get("/teams/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

# Get a specific team by ID
@router.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Update team information
@router.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, current_user: schemas.Player = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is the captain of the team (only captain can update team info)
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if current_user.id != db_team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can update team information")
    db_team.name = team.name
    db.commit()
    db.refresh(db_team)
    return db_team

# Delete a team
@router.delete("/teams/{team_id}", response_model=schemas.Team)
def delete_team(team_id: int, current_user: schemas.Player = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is the captain of the team (only captain can delete team)
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if current_user.id != db_team.captain_id:
        raise HTTPException(status_code=403, detail="Only the captain can delete the team")
    db.delete(db_team)
    db.commit()
    return db_team
