---
description: Merge a LoRA adapter into the base model and save the merged weights
argument-hint: <adapter-path> <output-path>  e.g. models/adapters/phi2-lora models/merged/phi2-merged
---

Merge LoRA adapter weights into the base model. This produces a standalone model that doesn't need PEFT at inference time and can be pushed directly to the Hub.

Parse arguments: `$ARGUMENTS`

```python
import sys
args = "$ARGUMENTS".split()
if len(args) != 2:
    print("Usage: /merge-lora <adapter-path> <output-path>")
    sys.exit(1)

adapter_path, output_path = args
from app.services.lora_service import merge_and_save
merge_and_save(adapter_path, output_path)
print(f"Merged model saved to: {output_path}")
```

Note: Merging requires loading the full base model in fp16 on CPU — this may need 14–30 GB RAM depending on model size.
