"""Tests for REST API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch


@pytest.fixture
def app():
    # Patch model loading so tests don't require a GPU
    with patch("app.services.model_service.ModelService.load"):
        from app.main import app as fastapi_app
        yield fastapi_app


@pytest.mark.asyncio
async def test_root(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "chat_ui" in data


@pytest.mark.asyncio
async def test_health(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "device" in data


@pytest.mark.asyncio
async def test_models_current_not_loaded(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/api/models/current")
    assert r.status_code == 200
    assert r.json()["loaded"] is False
