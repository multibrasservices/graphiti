# server/graph_service/main.py - VERSION SÉCURISÉE

from contextlib import asynccontextmanager
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse

from graph_service.config import get_settings
from graph_service.routers import ingest, retrieve
from graph_service.zinc.graphiti import initialize_graphiti

# --- DÉBUT DE L'AJOUT DE SÉCURITÉ ---

# On définit le nom de l'en-tête que le client devra envoyer.
# C'est un standard d'utiliser "X-API-Key".
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Cette fonction est notre "videur". Elle est appelée pour chaque requête.
    """
    settings = get_settings()
    
    # Si aucune clé n'est définie sur le serveur, on laisse passer tout le monde.
    if not settings.GRAPHITI_API_KEY:
        return api_key

    # Si une clé est définie, on la compare avec celle envoyée par le client.
    if api_key == settings.GRAPHITI_API_KEY:
        return api_key
    else:
        # Si les clés ne correspondent pas, on bloque l'accès.
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
    # Shutdown
    # No need to close Graphiti here, as it's handled per-request


# On ajoute 'dependencies=[Security(get_api_key)]' pour activer notre "videur"
# sur TOUTES les routes de l'API, sauf le healthcheck.
app = FastAPI(lifespan=lifespan, dependencies=[Security(get_api_key)])


app.include_router(retrieve.router)
app.include_router(ingest.router)


# On laisse le healthcheck en dehors de la sécurité pour que Coolify puisse l'utiliser.
@app.get('/healthcheck', include_in_schema=False)
async def healthcheck():
    return JSONResponse(content={'status': 'healthy'}, status_code=200)
