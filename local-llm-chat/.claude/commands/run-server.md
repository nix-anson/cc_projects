---
description: Start the FastAPI server with uvicorn
---

Start the local LLM chat server.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Once running:
- Chat UI:   http://localhost:8000/static/index.html
- API docs:  http://localhost:8000/docs
- Health:    http://localhost:8000/health
- WebSocket: ws://localhost:8000/ws/chat

The model configured in `.env` (`BASE_MODEL_ID`) will load at startup.
Loading time depends on model size and available hardware.

For a faster startup during development with a specific adapter:
```bash
LORA_ADAPTER_PATH=models/adapters/phi2-lora uvicorn app.main:app --reload
```
