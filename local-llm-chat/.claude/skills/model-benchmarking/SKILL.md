---
description: Measure model perplexity, generation throughput, and latency. Use when the user asks how fast the model is, wants to compare before/after fine-tuning, or needs to benchmark two adapters.
allowed-tools: Read, Write, Glob, Bash
---

# Model Benchmarking Skill

## Metrics to Measure

1. **Perplexity** — lower is better; measures how well the model predicts the test set
2. **Tokens/second** — generation throughput
3. **Time to first token (TTFT)** — latency before streaming begins
4. **Peak VRAM** — GPU memory high watermark

## Perplexity Calculation

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import math

def compute_perplexity(model_id, test_texts, max_length=512, device="cuda"):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map=device, trust_remote_code=True)
    model.eval()

    total_loss = 0.0
    total_tokens = 0

    with torch.no_grad():
        for text in test_texts:
            enc = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
            enc = {k: v.to(device) for k, v in enc.items()}
            labels = enc["input_ids"].clone()
            output = model(**enc, labels=labels)
            n_tokens = (labels != -100).sum().item()
            total_loss += output.loss.item() * n_tokens
            total_tokens += n_tokens

    avg_loss = total_loss / total_tokens
    return math.exp(avg_loss)

# Usage:
# ppl = compute_perplexity("models/adapters/phi2-lora", test_texts)
# print(f"Perplexity: {ppl:.2f}")
```

## Throughput Benchmark

```python
import time, asyncio
from app.services.model_service import model_service

async def benchmark_throughput(prompts: list[str], warmup: int = 1):
    # Warmup
    for p in prompts[:warmup]:
        async for _ in model_service.stream_generate(p):
            pass

    times = []
    token_counts = []

    for prompt in prompts[warmup:]:
        tokens = []
        t0 = time.perf_counter()
        async for tok in model_service.stream_generate(prompt):
            if not tokens:
                print(f"TTFT: {time.perf_counter() - t0:.3f}s")
            tokens.append(tok)
        elapsed = time.perf_counter() - t0
        times.append(elapsed)
        token_counts.append(len(tokens))

    avg_tps = sum(token_counts) / sum(times)
    print(f"Average throughput: {avg_tps:.1f} tok/s")
    print(f"Average latency:    {sum(times)/len(times):.2f}s")
    return avg_tps
```

## Comparing Base vs Fine-tuned

Run perplexity on the same held-out test set:
1. Load base model, compute perplexity → `ppl_base`
2. Load adapter, compute perplexity → `ppl_finetuned`
3. Report improvement: `delta = ppl_base - ppl_finetuned`

A meaningful improvement is typically >10% reduction in perplexity on domain-specific data.

## VRAM Profiling

```python
import torch

def profile_vram(device="cuda"):
    torch.cuda.reset_peak_memory_stats(device)
    # ... run generation ...
    peak = torch.cuda.max_memory_allocated(device) / (1024**3)
    print(f"Peak VRAM: {peak:.2f} GB")
```
