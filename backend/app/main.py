from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="An evidence-grounded AI research copilot.",
)

app.include_router(
    health_router,
    prefix="/api/v1",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Welcome to PaperPilot Pro",
        "docs": "/docs",
    }
