# server/graph_service/main.py - VERSION CORRIGÉE

from contextlib import asynccontextmanager
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse

from graph_service.config import get_settings
from graph_service.routers import ingest, retrieve
# --- CORRECTION DE LA FAUTE DE FRAPPE ICI ---
from graph_service.zep.graphiti import initialize_graphiti

# --- DÉBUT DE L'AJOUT DE SÉCURITÉ ---

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    settings = get_settings()
    
    if not settings.graphiti_api_key:
        return api_key

    if api_key == settings.graphiti_api_key:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# --- FIN DE L'AJOUT DE SÉCURITÉ ---


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    await initialize_graphiti(settings)
    yield


app = FastAPI(lifespan=lifespan, dependencies=[Security(get_api_key)])


app.include_router(retrieve.router)
app.include_router(ingest.router)


@app.get('/healthcheck', include_in_schema=False)
async def healthcheck():
    return JSONResponse(content={'status': 'healthy'}, status_code=200)
