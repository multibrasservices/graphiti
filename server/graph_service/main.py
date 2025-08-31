# server/graph_service/main.py - VERSION FINALE AVEC HEALTHCHECK PUBLIC

from contextlib import asynccontextmanager
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse

from graph_service.config import get_settings
from graph_service.routers import ingest, retrieve
from graph_service.zep_graphiti import initialize_graphiti

# --- DÉBUT DE LA SÉCURITÉ ---

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

# --- FIN DE LA SÉCURITÉ ---


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    await initialize_graphiti(settings)
    yield


# On crée l'application SANS la sécurité pour l'instant
app = FastAPI(lifespan=lifespan)


# --- CORRECTION ICI ---
# On déplace le healthcheck AVANT d'inclure les routeurs sécurisés.
# Il ne sera donc pas protégé par la dépendance.
@app.get('/healthcheck', include_in_schema=False)
async def healthcheck():
    return JSONResponse(content={'status': 'healthy'}, status_code=200)


# Maintenant, on inclut les routeurs qui ont besoin de sécurité,
# en leur appliquant notre "videur" directement.
app.include_router(retrieve.router, dependencies=[Security(get_api_key)])
app.include_router(ingest.router, dependencies=[Security(get_api_key)])
