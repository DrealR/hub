"""Main application entry point."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.config import settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="{{PROJECT_DESCRIPTION}}",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        """Root endpoint with project information."""
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "message": "{{PROJECT_NAME}} is running",
            "guardian_framework": "Active",
            "docs": "/docs",
            "health": "/health"
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "timestamp": "{{CURRENT_DATE}}"}
    
    return app


def dev():
    """Run the application in development mode."""
    app = create_application()
    uvicorn.run(
        "src.{{PROJECT_SLUG}}.main:create_application",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()