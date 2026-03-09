"""Model information endpoints."""
from fastapi import APIRouter
from app.services.model_service import model_service

router = APIRouter(prefix="/api/models")


@router.get("/current")
async def get_current_model():
    if not model_service._loaded:
        return {"loaded": False, "model_id": None}
    return {
        "loaded": True,
        "model_id": model_service._model_id,
        "device": model_service.device,
    }
