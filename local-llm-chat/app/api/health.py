"""Health-check endpoint with GPU diagnostics."""
from fastapi import APIRouter
from app.core.gpu_utils import get_device_info
from app.services.model_service import model_service

router = APIRouter()


@router.get("/health")
async def health():
    device_info = get_device_info()
    return {
        "status": "ok",
        "model_loaded": model_service._loaded,
        "model_id": model_service._model_id if model_service._loaded else None,
        "device": model_service.device,
        **device_info,
    }
