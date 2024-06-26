from fastapi import FastAPI
from src.routers import partidos,deportes,jugadores,equipos,escenarios,estadisticas
from src.config.database import init_db
from fastapi.security import HTTPBearer

app = FastAPI()

app.title = "DEPORTESUAM API"
app.summary = "DEPORTESUAM APIREST API with FastAPI and Python"
app.description = "This is a demonstration of API REST using Python"
app.version = "1.0.0"
app.contact = {
    "name": "Johan Polo and Luis Canon",
}


app.include_router(partidos.router, prefix="/matches")
app.include_router(deportes.router, prefix="/sports")
app.include_router(jugadores.router, prefix="/players")
app.include_router(equipos.router, prefix="/teams")
app.include_router(escenarios.router, prefix="/scenarios")
app.include_router(estadisticas.router, prefix="/statistics")


security = HTTPBearer()

app.openapi_schema = app.openapi()



@app.on_event("startup")
def on_startup():
    init_db()  