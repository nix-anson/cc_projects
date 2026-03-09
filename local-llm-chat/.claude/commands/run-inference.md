---
description: One-shot inference with tokens/sec benchmark
argument-hint: <prompt>  e.g. "What is quantization in machine learning?"
---

Run a single inference pass and measure throughput.

```python
import time, asyncio
from app.services.model_service import model_service
from app.core.config import settings

# Load model if not already loaded
if not model_service._loaded:
    print(f"Loading {settings.base_model_id}...")
    model_service.load()

prompt = "$ARGUMENTS"
print(f"\nPrompt: {prompt}\n\nResponse:\n")

tokens = []
t0 = time.perf_counter()

async def run():
    async for token in model_service.stream_generate(prompt):
        print(token, end="", flush=True)
        tokens.append(token)

asyncio.run(run())

elapsed = time.perf_counter() - t0
full_text = "".join(tokens)
tok_count = len(full_text.split())  # rough word count as proxy

print(f"\n\n--- Stats ---")
print(f"Tokens (approx): {tok_count}")
print(f"Time: {elapsed:.2f}s")
print(f"Throughput: {tok_count / elapsed:.1f} tok/s")
```
