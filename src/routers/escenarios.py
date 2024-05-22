from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas import escenarios as schemas
from ..models import escenarios as models
from ..config import database

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new venue
@router.post("/venues/", response_model=schemas.Venue, tags=["escenarios"])
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    db_venue = models.Venue(**venue.dict())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

# Get all venues
@router.get("/venues/", response_model=List[schemas.Venue], tags=["escenarios"])
def read_venues(db: Session = Depends(get_db)):
    venues = db.query(models.Venue).all()
    return venues

# Get a specific venue by ID
@router.get("/venues/{venue_id}", response_model=schemas.Venue, tags=["escenarios"])
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

# Update venue information
@router.put("/venues/{venue_id}", response_model=schemas.Venue, tags=["escenarios"])
def update_venue(venue_id: int, venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    for var, value in vars(venue).items():
        setattr(db_venue, var, value)
    db.commit()
    db.refresh(db_venue)
    return db_venue

# Delete a venue
@router.delete("/venues/{venue_id}", response_model=schemas.Venue, tags=["escenarios"])
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    db.delete(db_venue)
    db.commit()
    return db_venue
