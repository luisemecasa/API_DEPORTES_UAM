from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "sqlite:///./database.sqlite"

engine = create_engine(
    database_url, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    from ..models import jugadores, deportes, equipos, escenarios, estadisticas, partidos
    Base.metadata.create_all(bind=engine)
