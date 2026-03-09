---
description: Download a HuggingFace model to models/base/
argument-hint: <model-id>  e.g. microsoft/phi-2
---

Download the model `$ARGUMENTS` from HuggingFace Hub into `models/base/`.

Steps:
1. Run the following Python snippet to download and cache the model weights locally:

```python
from huggingface_hub import snapshot_download
import os

model_id = "$ARGUMENTS"
local_dir = f"models/base/{model_id.replace('/', '--')}"
os.makedirs(local_dir, exist_ok=True)

token = os.getenv("HF_TOKEN") or None
print(f"Downloading {model_id} -> {local_dir}")
snapshot_download(repo_id=model_id, local_dir=local_dir, token=token)
print("Download complete.")
```

2. After downloading, update `BASE_MODEL_ID` in `.env` to point to the local path:
   ```
   BASE_MODEL_ID=models/base/<model-id-with-dashes>
   ```

3. Restart the server for the new model to load.

Note: For gated models (Llama 3, Mistral) ensure `HF_TOKEN` is set in `.env`.
