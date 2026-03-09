"""WebSocket endpoint for real-time LLM token streaming."""
from __future__ import annotations

import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.model_service import model_service

logger = logging.getLogger(__name__)
router = APIRouter()


class StreamingConnectionManager:
    """Tracks active WebSocket connections (one model, many concurrent clients)."""

    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.add(ws)
        logger.info(f"WS connected. Total: {len(self.active)}")

    def disconnect(self, ws: WebSocket) -> None:
        self.active.discard(ws)
        logger.info(f"WS disconnected. Total: {len(self.active)}")

    async def send(self, ws: WebSocket, payload: dict) -> None:
        try:
            await ws.send_text(json.dumps(payload))
        except Exception:
            self.disconnect(ws)


manager = StreamingConnectionManager()


@router.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming LLM responses token-by-token.

    Client → Server messages:
        {"type": "chat", "message": "...", "history": [...]}
        {"type": "cancel"}

    Server → Client messages:
        {"type": "token", "text": "..."}
        {"type": "done"}
        {"type": "error", "message": "..."}
    """
    await manager.connect(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await manager.send(websocket, {"type": "error", "message": "Invalid JSON"})
                continue

            msg_type = data.get("type")

            if msg_type == "chat":
                user_message = data.get("message", "").strip()
                history = data.get("history", [])

                if not user_message:
                    await manager.send(websocket, {"type": "error", "message": "Empty message"})
                    continue

                if not model_service._loaded:
                    await manager.send(
                        websocket,
                        {"type": "error", "message": "Model not loaded. Check server logs."},
                    )
                    continue

                try:
                    async for token in model_service.stream_generate(user_message, history=history):
                        await manager.send(websocket, {"type": "token", "text": token})
                    await manager.send(websocket, {"type": "done"})
                except Exception as e:
                    logger.exception("Generation error")
                    await manager.send(websocket, {"type": "error", "message": str(e)})

            elif msg_type == "cancel":
                # Future: signal cancellation via threading.Event
                await manager.send(websocket, {"type": "done"})

            else:
                await manager.send(
                    websocket, {"type": "error", "message": f"Unknown message type: {msg_type}"}
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
