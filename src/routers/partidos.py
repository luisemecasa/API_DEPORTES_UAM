from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import partidos as schemas
from ..models import partidos as models
from ..config import database
from typing import List  
router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match




@router.get("/matches/", response_model=List[schemas.Match])
def read_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).all()
    return matches


@router.get("/matches/{match_id}", response_model=schemas.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    for var, value in vars(match).items():
        setattr(db_match, var, value)
    db.commit()
    db.refresh(db_match)
    return db_match

# Delete a match
@router.delete("/matches/{match_id}", response_model=schemas.Match)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return db_match
