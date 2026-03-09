---
description: Implement or debug TextIteratorStreamer → asyncio.Queue → WebSocket token streaming pipelines. Use when adding streaming to new endpoints, debugging streaming gaps/hangs, or implementing cancellation support.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Token Streaming Pipeline Skill

## Architecture Overview

```
model.generate(streamer=streamer)      ← background thread 1
       ↓
TextIteratorStreamer                    ← queue-based buffer (internal)
       ↓
for token in streamer: queue.put(token) ← background thread 2
       ↓ call_soon_threadsafe
asyncio.Queue                          ← async-safe bridge
       ↓ await queue.get()
WebSocket.send_text({"type":"token"}) ← async event loop
```

## Reference Implementation

The canonical implementation lives in `app/services/model_service.py` → `stream_generate()` and `app/websockets/chat_ws.py`.

Always read these files before modifying the streaming pipeline.

## Complete Pattern (copy-paste ready)

```python
import asyncio, threading
from transformers import TextIteratorStreamer

async def stream_generate(model, tokenizer, inputs, device, **gen_kwargs):
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def _generate():
        try:
            model.generate(**inputs.to(device), streamer=streamer, **gen_kwargs)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

    def _drain():
        for token in streamer:
            loop.call_soon_threadsafe(queue.put_nowait, token)

    threading.Thread(target=_generate, daemon=True).start()
    threading.Thread(target=_drain, daemon=True).start()

    while True:
        item = await queue.get()
        if item is None:
            break
        if item:
            yield item
```

## Common Issues and Fixes

### Streaming hangs / no tokens appear
- Ensure `streamer` is passed to `model.generate()` as a keyword argument
- Ensure `_generate` and `_drain` threads are started **before** `await queue.get()`
- Check that `loop.call_soon_threadsafe` uses the correct event loop (get it before spawning threads)

### Duplicate tokens or prompt included
- Set `skip_prompt=True` on `TextIteratorStreamer`
- Set `skip_special_tokens=True` to remove EOS/PAD tokens

### WebSocket disconnects mid-stream
- Wrap `ws.send_text()` in try/except
- On disconnect, set a `threading.Event` that a custom `StoppingCriteria` checks

### Empty tokens sent to client
- Filter with `if token:` before yielding — some tokenizers emit empty strings

## Cancellation Implementation

```python
cancel_event = threading.Event()

class CancelCriteria(StoppingCriteria):
    def __call__(self, input_ids, scores, **kwargs):
        return cancel_event.is_set()

# In WebSocket handler, on {"type": "cancel"}:
cancel_event.set()
```
