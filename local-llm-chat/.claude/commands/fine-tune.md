---
description: Run LoRA/QLoRA fine-tuning with a YAML config
argument-hint: <path/to/config.yaml>  e.g. configs/phi_lora.yaml
---

Start a fine-tuning run using the config at `$ARGUMENTS`.

Run:
```bash
python training/train.py --config $ARGUMENTS
```

Before running, verify:
- The `base_model_id` in the config is accessible (local or HF Hub)
- `output_dir` path exists or will be created automatically
- `dataset_name` or `dataset_path` is set
- For 4-bit training: `bitsandbytes` is installed and a CUDA GPU is available

Available configs:
- `configs/phi_lora.yaml` — Phi-2 (2.7B) — ~8GB VRAM
- `configs/mistral_lora.yaml` — Mistral-7B — ~12GB VRAM (needs HF_TOKEN)
- `configs/llama_qlora.yaml` — Llama-3.1-8B — ~10GB VRAM (needs HF_TOKEN)

Monitor progress in `logs/` or with `/monitor-training`.
