from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import deportes as schemas
from ..models import deportes as models
from ..config import database

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new sport
@router.post("/sports/", response_model=schemas.Sport)
def create_sport(sport: schemas.SportCreate, db: Session = Depends(get_db)):
    db_sport = models.Sport(name=sport.name)
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport

# Get all sports
@router.get("/sports/", response_model=List[schemas.Sport])
def read_sports(db: Session = Depends(get_db)):
    sports = db.query(models.Sport).all()
    return sports

# Get a specific sport by ID
@router.get("/sports/{sport_id}", response_model=schemas.Sport)
def read_sport(sport_id: int, db: Session = Depends(get_db)):
    sport = db.query(models.Sport).filter(models.Sport.id == sport_id).first()
    if sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")
    return sport

# Update sport information
@router.put("/sports/{sport_id}", response_model=schemas.Sport)
def update_sport(sport_id: int, sport: schemas.SportCreate, db: Session = Depends(get_db)):
    db_sport = db.query(models.Sport).filter(models.Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")
    db_sport.name = sport.name
    db.commit()
    db.refresh(db_sport)
    return db_sport

# Delete a sport
@router.delete("/sports/{sport_id}", response_model=schemas.Sport)
def delete_sport(sport_id: int, db: Session = Depends(get_db)):
    db_sport = db.query(models.Sport).filter(models.Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")
    db.delete(db_sport)
    db.commit()
    return db_sport
