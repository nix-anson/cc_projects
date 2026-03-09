---
description: Generate LoRA/QLoRA training configs and SFTTrainer setup code. Use when creating new YAML experiment configs, setting up a training pipeline, choosing LoRA hyperparameters, or scaffolding training/train.py.
allowed-tools: Read, Write, Edit, Glob
---

# LoRA Training Setup Skill

## Purpose
Generate production-ready LoRA fine-tuning configurations and SFTTrainer code based on the target model, available VRAM, and dataset characteristics.

## Config Generation Template

When generating a new YAML config, gather:
1. **Model ID** — base model to fine-tune
2. **VRAM budget** — determines quantization and batch size
3. **Dataset** — HF Hub name or local path
4. **Task** — instruction-following, classification, code generation, etc.

Then generate a YAML file at `configs/<model-slug>_lora.yaml` following this structure:

```yaml
base_model_id: "<model-id>"
hf_token: ""

dataset_name: "<hf-dataset-id>"
dataset_split: "train"
text_column: "text"
max_seq_length: 2048

output_dir: "models/adapters/<run-name>"
logging_dir: "logs/<run-name>"

num_train_epochs: 3
per_device_train_batch_size: <4 for ≥8GB, 2 for <8GB, 1 for <6GB>
gradient_accumulation_steps: <8 if batch=1, 4 if batch=2, 2 if batch=4>
learning_rate: <2e-4 for small models, 1e-4 for 7B+>
warmup_ratio: 0.05
lr_scheduler_type: "cosine"
save_steps: 100
logging_steps: 10
fp16: false
bf16: true

lora:
  r: <16 for ≤3B, 32 for 7B, 64 for 13B+>
  lora_alpha: <2 * r>
  lora_dropout: 0.05
  target_modules: <see model-specific list below>
  bias: "none"
  task_type: "CAUSAL_LM"

quantization:
  load_in_4bit: true
  bnb_4bit_quant_type: "nf4"
  bnb_4bit_use_double_quant: true
  bnb_4bit_compute_dtype: "bfloat16"
```

## Target Modules by Architecture

| Architecture | Target Modules |
|-------------|---------------|
| LLaMA / Mistral | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` |
| Phi-2 | `q_proj, v_proj, k_proj, dense` |
| GPT-2 / GPT-Neo | `c_attn, c_proj` |
| Falcon | `query_key_value, dense` |
| Gemma | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` |

## Effective Batch Size

Always maintain: `effective_batch = per_device_train_batch_size × gradient_accumulation_steps × num_gpus`

Recommended effective batch size: 16–32 for most instruction-tuning tasks.

## After Generating Config

Tell the user to start training with:
```
/fine-tune configs/<config-name>.yaml
```

And monitor with:
```
/monitor-training
```
