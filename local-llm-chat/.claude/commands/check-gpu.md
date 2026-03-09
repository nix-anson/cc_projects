---
description: Run CUDA diagnostics and show VRAM usage
---

Print a full GPU/CUDA report for this machine.

```python
from app.core.gpu_utils import get_device_info
import json

info = get_device_info()
print(json.dumps(info, indent=2))

if info["cuda_available"]:
    for gpu in info["gpus"]:
        pct = (gpu["reserved_gb"] / gpu["total_vram_gb"]) * 100
        bar = "#" * int(pct / 5) + "." * (20 - int(pct / 5))
        print(f"\n  GPU {gpu['index']}: {gpu['name']}")
        print(f"  [{bar}] {pct:.1f}% used")
        print(f"  Total: {gpu['total_vram_gb']} GB  |  Free: {gpu['free_gb']} GB")
elif info["mps_available"]:
    print("\nApple MPS (Metal) is available.")
else:
    print("\nNo GPU detected — running on CPU.")
```

Model VRAM requirements (approximate at 4-bit):
| Model        | Params | Min VRAM |
|-------------|--------|---------|
| Phi-2        | 2.7B   | 4 GB    |
| Mistral-7B   | 7B     | 6 GB    |
| Llama-3.1-8B | 8B     | 8 GB    |
