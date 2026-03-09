"""Fine-tuning entry point.

Usage:
    python training/train.py --config configs/phi_lora.yaml
"""
from __future__ import annotations

import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Fine-tune an LLM with LoRA/QLoRA")
    parser.add_argument("--config", required=True, help="Path to YAML training config")
    args = parser.parse_args()

    from training.config import TrainingConfig
    from training.dataset import prepare_dataset
    from training.callbacks import LossLoggerCallback, BestModelCallback

    cfg = TrainingConfig.from_yaml(args.config)
    logger.info(f"Training config loaded: {args.config}")
    logger.info(f"  model   : {cfg.base_model_id}")
    logger.info(f"  output  : {cfg.output_dir}")
    logger.info(f"  epochs  : {cfg.num_train_epochs}")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer, SFTConfig

    # ── Quantization ──────────────────────────────────────────────────────────
    compute_dtype = getattr(torch, cfg.quantization.bnb_4bit_compute_dtype, torch.bfloat16)
    bnb_config = None
    if cfg.quantization.load_in_4bit and torch.cuda.is_available():
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=cfg.quantization.bnb_4bit_quant_type,
            bnb_4bit_use_double_quant=cfg.quantization.bnb_4bit_use_double_quant,
            bnb_4bit_compute_dtype=compute_dtype,
        )

    # ── Tokenizer ─────────────────────────────────────────────────────────────
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        cfg.base_model_id,
        trust_remote_code=True,
        token=cfg.hf_token or None,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ── Base model ────────────────────────────────────────────────────────────
    logger.info("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        cfg.base_model_id,
        quantization_config=bnb_config,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
        token=cfg.hf_token or None,
    )

    if bnb_config:
        model = prepare_model_for_kbit_training(model)

    # ── LoRA ──────────────────────────────────────────────────────────────────
    peft_config = LoraConfig(
        r=cfg.lora.r,
        lora_alpha=cfg.lora.lora_alpha,
        lora_dropout=cfg.lora.lora_dropout,
        target_modules=cfg.lora.target_modules,
        bias=cfg.lora.bias,
        task_type=cfg.lora.task_type,
    )

    # ── Dataset ───────────────────────────────────────────────────────────────
    logger.info("Loading dataset...")
    dataset = prepare_dataset(cfg)
    logger.info(f"Dataset size: {len(dataset)} examples")

    # ── Trainer ───────────────────────────────────────────────────────────────
    sft_config = SFTConfig(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type=cfg.lr_scheduler_type,
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        fp16=cfg.fp16,
        bf16=cfg.bf16,
        logging_dir=cfg.logging_dir,
        dataset_text_field=cfg.text_column,
        max_seq_length=cfg.max_seq_length,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        callbacks=[LossLoggerCallback(), BestModelCallback()],
    )

    logger.info("Starting training...")
    trainer.train()

    logger.info(f"Saving final adapter to {cfg.output_dir}")
    trainer.save_model(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)
    logger.info("Training complete.")


if __name__ == "__main__":
    main()
