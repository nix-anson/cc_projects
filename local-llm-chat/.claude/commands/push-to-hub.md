---
description: Push a LoRA adapter to HuggingFace Hub
argument-hint: <adapter-path> <repo-id>  e.g. models/adapters/phi2-lora yourname/phi2-lora-guanaco
---

Upload a LoRA adapter directory to HuggingFace Hub.

Parse arguments: `$ARGUMENTS`

```python
import sys, os
args = "$ARGUMENTS".split()
if len(args) != 2:
    print("Usage: /push-to-hub <adapter-path> <repo-id>")
    sys.exit(1)

adapter_path, repo_id = args
token = os.getenv("HF_TOKEN")
if not token:
    print("Error: HF_TOKEN environment variable not set.")
    sys.exit(1)

from app.services.lora_service import push_adapter_to_hub
push_adapter_to_hub(adapter_path, repo_id, token=token)
```

Prerequisites:
- `HF_TOKEN` must be set in `.env` with write access
- The adapter directory must contain `adapter_config.json` and `adapter_model.safetensors`
