"""FastAPI application entry point with lifespan model loading."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import health, models
from app.core.config import settings
from app.services.model_service import model_service
from app.websockets.chat_ws import router as ws_router

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model at startup; release GPU memory at shutdown."""
    logger.info("Starting up — loading model...")
    try:
        model_service.load(
            model_id=settings.base_model_id,
            lora_adapter_path=settings.lora_adapter_path or None,
        )
    except Exception as e:
        logger.error(f"Model failed to load: {e}")
        logger.warning("Server starting without a loaded model. /health will reflect this.")

    yield

    logger.info("Shutting down — unloading model...")
    model_service.unload()


app = FastAPI(
    title="Local LLM Chat",
    description="Fine-tune and serve open-source LLMs with LoRA/QLoRA via FastAPI + WebSocket streaming.",
    version="0.1.0",
    lifespan=lifespan,
)

# Routers
app.include_router(health.router)
app.include_router(models.router)
app.include_router(ws_router)

# Serve the static chat UI at /static/index.html
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {
        "message": "Local LLM Chat API",
        "docs": "/docs",
        "chat_ui": "/static/index.html",
        "health": "/health",
        "websocket": "ws://localhost:8000/ws/chat",
    }
