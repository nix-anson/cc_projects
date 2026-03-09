---
description: Send a test message via WebSocket and print streamed tokens
argument-hint: <message>  e.g. "Explain LoRA in one paragraph"
---

Send the message `$ARGUMENTS` to the running server WebSocket and print all streamed tokens.

Run this Python snippet (requires `websockets` to be installed):

```python
import asyncio, json, websockets

async def chat(message):
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "chat", "message": message}))
        print(f"[user] {message}\n[assistant] ", end="", flush=True)
        while True:
            data = json.loads(await ws.recv())
            if data["type"] == "token":
                print(data["text"], end="", flush=True)
            elif data["type"] == "done":
                print()
                break
            elif data["type"] == "error":
                print(f"\nError: {data['message']}")
                break

asyncio.run(chat("$ARGUMENTS"))
```

Make sure the server is running (`/run-server`) before testing.
