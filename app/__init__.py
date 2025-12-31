from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router


def get_allowed_origins() -> list[str]:
    """Get allowed CORS origins based on environment."""
    if settings.DEV_MODE:
        return ["*"]

    print("CORS Origins:", settings.ALLOWED_ORIGINS)

    origins = settings.ALLOWED_ORIGINS
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router)

    return app
