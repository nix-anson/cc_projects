# Local LLM Chat — Claude Code Context

## Project Overview

Fine-tune open-source LLMs (Llama, Mistral, Phi) with LoRA/QLoRA and serve them via a FastAPI backend with real-time WebSocket token streaming and a single-page chat UI.

**Stack**: FastAPI · uvicorn · HuggingFace Transformers + PEFT + TRL · bitsandbytes · WebSockets · Pydantic Settings

---

## Directory Structure

```
local-llm-chat/
├── app/                        # FastAPI serving layer
│   ├── main.py                 # App entry + lifespan (model load/unload)
│   ├── core/
│   │   ├── config.py           # Pydantic Settings from .env
│   │   └── gpu_utils.py        # CUDA/MPS/CPU detection + VRAM info
│   ├── services/
│   │   ├── model_service.py    # Model loading + stream_generate()
│   │   └── lora_service.py     # Adapter merge + Hub upload
│   ├── api/
│   │   ├── health.py           # GET /health
│   │   └── models.py           # GET /api/models/current
│   └── websockets/
│       └── chat_ws.py          # /ws/chat WebSocket endpoint
├── training/                   # Fine-tuning pipeline
│   ├── train.py                # python training/train.py --config <yaml>
│   ├── config.py               # TrainingConfig dataclass
│   ├── dataset.py              # Dataset loading + formatting
│   └── callbacks.py            # Loss logging callbacks
├── configs/                    # Per-model LoRA YAML configs
│   ├── phi_lora.yaml           # Phi-2 2.7B (~4GB VRAM)
│   ├── mistral_lora.yaml       # Mistral-7B (~12GB VRAM)
│   └── llama_qlora.yaml        # Llama-3.1-8B (~10GB VRAM)
├── static/
│   └── index.html              # Single-page streaming chat UI
├── tests/
│   ├── test_api.py
│   └── test_streaming.py
├── models/                     # Gitignored — large binary files
│   ├── base/                   # Downloaded base model weights
│   └── adapters/               # LoRA checkpoints + merged models
└── data/                       # Gitignored
    ├── raw/
    └── processed/
```

---

## Architecture Decisions

### Streaming Pipeline
`TextIteratorStreamer` runs `model.generate()` in a background **thread** (blocking). A second thread drains the streamer and bridges tokens to an `asyncio.Queue` via `loop.call_soon_threadsafe()`. The async WebSocket handler awaits tokens from the queue.

**Never** run `model.generate()` directly in an async function — it blocks the event loop.

### Model Loading
One model per server process, loaded once in the FastAPI `lifespan` context manager and stored in the `model_service` singleton. To switch models, restart the server with a different `BASE_MODEL_ID` in `.env`.

### WebSocket Protocol
```
Client → Server: {"type": "chat", "message": "...", "history": [...]}
                 {"type": "cancel"}
Server → Client: {"type": "token",  "text": "..."}
                 {"type": "done"}
                 {"type": "error",  "message": "..."}
```

### Training Configs
YAML files per experiment under `configs/` — version-controllable and reproducible. Never use raw CLI flags for training.

---

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | App entry, lifespan, router registration |
| `app/core/config.py` | All settings via `.env` |
| `app/services/model_service.py` | `ModelService` class + `stream_generate()` |
| `app/websockets/chat_ws.py` | `StreamingConnectionManager` + `/ws/chat` |
| `training/train.py` | Fine-tuning entry point |
| `training/config.py` | `TrainingConfig` dataclass |

---

## Development Patterns

### Adding a New REST Endpoint
1. Create/edit a file in `app/api/`
2. Define Pydantic request/response models
3. Implement `async def` handler
4. Include router in `app/main.py`

### Modifying Streaming Behaviour
Always read `app/services/model_service.py` and `app/websockets/chat_ws.py` together — they are tightly coupled. Consult the `token-streaming` skill for the canonical pattern.

### Adding a New Training Config
Copy an existing YAML from `configs/`, adjust model ID and hyperparameters, save as `configs/<name>.yaml`. Run with `/fine-tune configs/<name>.yaml`.

---

## Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_MODEL_ID` | HF model ID or local path | `microsoft/phi-2` |
| `LORA_ADAPTER_PATH` | Path to LoRA adapter (optional) | `""` |
| `HF_TOKEN` | HuggingFace access token | `""` |
| `MAX_NEW_TOKENS` | Default generation length | `512` |
| `TEMPERATURE` | Sampling temperature | `0.7` |
| `TOP_P` | Nucleus sampling p | `0.9` |
| `DEBUG` | Enable debug logging | `false` |

---

## Code Style

- **Python 3.11+** with full type hints
- `from __future__ import annotations` in all files
- Async/await for all I/O; threading only for `model.generate()`
- Pydantic v2 models for all external data
- No bare `except:` — always catch specific exceptions or `Exception as e`
- `ruff` for linting, `black` for formatting

---

## Running the Project

```bash
# Install deps (install torch separately with CUDA first)
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

# Copy and configure env
cp .env.example .env
# Edit .env — set BASE_MODEL_ID and HF_TOKEN if needed

# Start server
uvicorn app.main:app --reload

# Open chat UI
# http://localhost:8000/static/index.html
```

---

## Available Slash Commands

| Command | What It Does |
|---------|-------------|
| `/download-model <id>` | Download model from HF Hub |
| `/fine-tune <config.yaml>` | Start a training run |
| `/run-server` | Start uvicorn dev server |
| `/test-chat <message>` | Send a test WebSocket message |
| `/check-gpu` | CUDA diagnostics + VRAM report |
| `/merge-lora <adapter> <output>` | Merge LoRA into base model |
| `/run-inference <prompt>` | One-shot inference + throughput |
| `/push-to-hub <adapter> <repo-id>` | Upload adapter to HF Hub |
| `/monitor-training` | Tail training logs |
| `/test-api` | Run pytest suite |

## Available Agents

| Agent | Expertise |
|-------|-----------|
| `finetuning-advisor` | LoRA hyperparameters, dataset quality, loss diagnosis |
| `streaming-architect` | TextIteratorStreamer + asyncio pipeline |
| `model-optimizer` | OOM fixes, quantization, Flash Attention |
| `api-designer` | FastAPI routes, Pydantic schemas, WS protocol |
| `hf-hub-expert` | Model search, gated access, adapter publishing |
