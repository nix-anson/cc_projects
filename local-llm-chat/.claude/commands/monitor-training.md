---
description: Tail training logs and display a live loss summary
---

Monitor an active or completed training run by tailing the most recent log file.

```python
import glob, os, re

log_dir = "logs"
log_files = sorted(glob.glob(f"{log_dir}/**/*.log", recursive=True), key=os.path.getmtime)
if not log_files:
    # Try trainer_log.jsonl output
    log_files = sorted(glob.glob(f"models/adapters/**/trainer_state.json", recursive=True), key=os.path.getmtime)

if not log_files:
    print("No log files found yet. Start a training run with /fine-tune first.")
else:
    latest = log_files[-1]
    print(f"Reading: {latest}\n")
    with open(latest) as f:
        content = f.read()

    # Parse loss values from trainer_state.json
    import json
    try:
        state = json.loads(content)
        history = state.get("log_history", [])
        print(f"{'Step':>8}  {'Loss':>10}  {'LR':>12}")
        print("-" * 34)
        for entry in history:
            if "loss" in entry:
                print(f"{entry['step']:>8}  {entry['loss']:>10.4f}  {entry.get('learning_rate', 0):>12.2e}")
        if history:
            last = [e for e in history if "loss" in e]
            if last:
                print(f"\nFinal loss: {last[-1]['loss']:.4f} at step {last[-1]['step']}")
    except json.JSONDecodeError:
        # Plain text log
        for line in content.splitlines()[-50:]:
            print(line)
```
