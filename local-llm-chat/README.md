# Local LLM Chat

Fine-tune open-source LLMs (Llama, Mistral, Phi) with LoRA/QLoRA and chat with them in real-time via a streaming WebSocket interface — all running locally.

## Features

- **LoRA/QLoRA fine-tuning** — train adapter weights on your own data with 4-bit quantization
- **Real-time token streaming** — WebSocket endpoint streams tokens as they're generated
- **Single-page chat UI** — zero build step, works immediately in any browser
- **Multi-model support** — YAML configs for Phi-2, Mistral-7B, and Llama-3.1-8B
- **FastAPI backend** — async, type-safe, with `/health` and `/docs`

## Hardware Requirements

| Model | Min VRAM | Recommended |
|-------|---------|-------------|
| Phi-2 (2.7B) | 4 GB | 6 GB |
| Mistral-7B | 6 GB | 10 GB |
| Llama-3.1-8B | 8 GB | 12 GB |
| CPU fallback | — | 16 GB RAM |

4-bit quantization (bitsandbytes) is enabled automatically when CUDA is available.

## Quick Start

### 1. Install Dependencies

```bash
# PyTorch with CUDA (adjust cu121 to your CUDA version)
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Project dependencies
pip install -r requirements.txt
```

For CPU-only (slower, no quantization):
```bash
pip install torch
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
BASE_MODEL_ID=microsoft/phi-2   # or a local path
HF_TOKEN=hf_...                 # required for gated models (Llama, Mistral)
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload
```

The model loads at startup (this may take 1–3 minutes the first time).

### 4. Open the Chat UI

Navigate to: **http://localhost:8000/static/index.html**

Type a message and press Enter to see tokens stream in real time.

---

## Fine-Tuning

### Prepare a Config

Choose one of the ready-made configs or create your own:

```bash
# Phi-2 (8GB VRAM, fastest)
python training/train.py --config configs/phi_lora.yaml

# Mistral-7B (12GB VRAM)
python training/train.py --config configs/mistral_lora.yaml

# Llama-3.1-8B (10GB VRAM, requires HF_TOKEN)
python training/train.py --config configs/llama_qlora.yaml
```

Edit the YAML to point to your dataset:
```yaml
dataset_name: "your-hf/dataset"   # HuggingFace dataset
# OR
dataset_path: "data/raw/my_data.jsonl"  # Local JSONL
```

The dataset should have a `text` column with formatted instruction pairs, or `instruction`/`output` columns (Alpaca format — auto-converted).

### Load the Adapter

After training, set in `.env`:
```env
LORA_ADAPTER_PATH=models/adapters/phi2-lora
```

Restart the server — the adapter loads on top of the base model.

### Merge and Export

```bash
python -c "
from app.services.lora_service import merge_and_save
merge_and_save('models/adapters/phi2-lora', 'models/merged/phi2-merged')
"
```

---

## API Reference

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/` | GET | Project info + links |
| `/health` | GET | GPU info, model status |
| `/api/models/current` | GET | Loaded model info |
| `/ws/chat` | WebSocket | Streaming chat |
| `/docs` | GET | Swagger UI |

### WebSocket Protocol

**Client → Server**
```json
{"type": "chat", "message": "Your message", "history": []}
{"type": "cancel"}
```

**Server → Client**
```json
{"type": "token", "text": "..."}
{"type": "done"}
{"type": "error", "message": "..."}
```

---

## Project Structure

```
local-llm-chat/
├── app/                    # FastAPI serving layer
│   ├── main.py             # App entry + lifespan
│   ├── core/               # Config + GPU utils
│   ├── services/           # Model loading + streaming
│   ├── api/                # REST endpoints
│   └── websockets/         # WebSocket handler
├── training/               # Fine-tuning pipeline
├── configs/                # YAML training configs
├── static/                 # Chat UI (index.html)
├── tests/                  # pytest tests
├── models/                 # Gitignored model weights
└── data/                   # Gitignored training data
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Claude Code Integration

This project includes Claude Code configuration in `.claude/`:

- **10 slash commands** — `/download-model`, `/fine-tune`, `/run-server`, `/test-chat`, `/check-gpu`, `/merge-lora`, `/run-inference`, `/push-to-hub`, `/monitor-training`, `/test-api`
- **5 specialized agents** — finetuning advisor, streaming architect, model optimizer, API designer, HF Hub expert
- **3 skills** — LoRA training setup, token streaming pipeline, model benchmarking

Open the project in VSCode and launch Claude Code to use them.
