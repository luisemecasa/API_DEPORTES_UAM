from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import jugadores as schemas
from ..models import jugadores as models
from ..config.database import get_db
from ..middlewares.auth import get_current_user, get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/players/", response_model=schemas.Player, tags=["jugadores"])
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = db.query(models.Player).filter(models.Player.email == player.email).first()
    if db_player:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(player.password)
    db_player = models.Player(name=player.name, email=player.email, hashed_password=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@router.post("/token", response_model=schemas.Token, tags=["jugadores"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Player).filter(models.Player.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/players/me/", response_model=schemas.Player, tags=["jugadores"])
def read_players_me(current_user: schemas.Player = Depends(get_current_user)):
    return current_user
