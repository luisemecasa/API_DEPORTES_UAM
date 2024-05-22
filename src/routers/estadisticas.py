from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import estadisticas as schemas
from ..models import estadisticas as models
from ..config import database
from typing import List

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create new statistics
@router.post("/statistics/", response_model=schemas.Statistic, tags=["statistics"])
def create_statistics(statistic: schemas.StatisticCreate, db: Session = Depends(get_db)):
    db_statistic = models.Statistic(**statistic.dict())
    db.add(db_statistic)
    db.commit()
    db.refresh(db_statistic)
    return db_statistic

# Get all statistics
@router.get("/statistics/", response_model=List[schemas.Statistic], tags=["statistics"])
def read_statistics(db: Session = Depends(get_db)):
    statistics = db.query(models.Statistic).all()
    return statistics

# Get statistics for a specific match
@router.get("/statistics/match/{match_id}", response_model=List[schemas.Statistic], tags= ["statistics"])
def read_statistics_by_match(match_id: int, db: Session = Depends(get_db)):
    statistics = db.query(models.Statistic).filter(models.Statistic.match_id == match_id).all()
    return statistics

# Get statistics for a specific player
@router.get("/statistics/player/{player_id}", response_model=List[schemas.Statistic], tags=["statistics"])
def read_statistics_by_player(player_id: int, db: Session = Depends(get_db)):
    statistics = db.query(models.Statistic).filter(models.Statistic.player_id == player_id).all()
    return statistics

# Update statistics
@router.put("/statistics/{statistic_id}", response_model=schemas.Statistic, tags=["statistics"])
def update_statistics(statistic_id: int, statistic: schemas.StatisticCreate, db: Session = Depends(get_db)):
    db_statistic = db.query(models.Statistic).filter(models.Statistic.id == statistic_id).first()
    if db_statistic is None:
        raise HTTPException(status_code=404, detail="Statistic not found")
    for var, value in vars(statistic).items():
        setattr(db_statistic, var, value)
    db.commit()
    db.refresh(db_statistic)
    return db_statistic

# Delete statistics
@router.delete("/statistics/{statistic_id}", response_model=schemas.Statistic, tags= ["statistics"])
def delete_statistics(statistic_id: int, db: Session = Depends(get_db)):
    db_statistic = db.query(models.Statistic).filter(models.Statistic.id == statistic_id).first()
    if db_statistic is None:
        raise HTTPException(status_code=404, detail="Statistic not found")
    db.delete(db_statistic)
    db.commit()
    return db_statistic
