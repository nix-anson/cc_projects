"""Tests for the WebSocket streaming endpoint."""
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with patch("app.services.model_service.ModelService.load"):
        from app.main import app
        with TestClient(app) as c:
            yield c


def test_ws_chat_model_not_loaded(client):
    """When no model is loaded, the WS should return an error message."""
    with client.websocket_connect("/ws/chat") as ws:
        ws.send_text(json.dumps({"type": "chat", "message": "Hello"}))
        data = json.loads(ws.receive_text())
        assert data["type"] == "error"
        assert "not loaded" in data["message"].lower()


def test_ws_invalid_json(client):
    with client.websocket_connect("/ws/chat") as ws:
        ws.send_text("not json")
        data = json.loads(ws.receive_text())
        assert data["type"] == "error"


def test_ws_unknown_message_type(client):
    with client.websocket_connect("/ws/chat") as ws:
        ws.send_text(json.dumps({"type": "unknown"}))
        data = json.loads(ws.receive_text())
        assert data["type"] == "error"
