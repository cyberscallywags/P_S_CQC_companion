"""FastAPI application with Logfire observability and Neo4j integration.

Returns:
    _type_: _description_
"""

import logfire
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from services.graph_service import GraphService

# Initialize graph service
graph_service = GraphService(
    uri=settings.neo4j_uri,
    username=settings.neo4j_user,
    password=settings.neo4j_password,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logfire.info("Starting up application")
    try:
        await graph_service.connect()
    except Exception as e:
        logfire.error("Failed to connect to graph database", error=str(e))
        raise
    yield
    # Shutdown
    logfire.info("Shutting down application")
    await graph_service.disconnect()


# Initialize Logfire for observability
logfire.configure(
    project_name=settings.logfire_project_name,
    token=settings.logfire_token,
)

app = FastAPI(lifespan=lifespan)

# Instrument FastAPI with Logfire
logfire.instrument_fastapi(app)


@app.get("/health")
async def root():
    """Health check endpoint.

    Returns:
        json: A message indicating that the API and database health status.
    """
    logfire.info("Health check called")
    db_healthy = await graph_service.health_check()
    return {
        "msg": "API is healthy",
        "database": "healthy" if db_healthy else "unhealthy",
    }
