"""API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_status():
    """Get API status."""
    return {
        "status": "operational",
        "service": "{{PROJECT_NAME}}",
        "version": "1.0.0"
    }


@router.get("/items")
async def get_items():
    """Get sample items."""
    return {
        "items": [
            {"id": 1, "name": "Sample Item 1"},
            {"id": 2, "name": "Sample Item 2"},
        ]
    }