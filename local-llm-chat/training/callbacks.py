"""Custom HuggingFace Trainer callbacks for logging and checkpointing."""
from __future__ import annotations

import logging
from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments

logger = logging.getLogger(__name__)


class LossLoggerCallback(TrainerCallback):
    """Print training loss at each logging step."""

    def on_log(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        logs: dict | None = None,
        **kwargs,
    ):
        if logs is None:
            return
        step = state.global_step
        loss = logs.get("loss")
        lr = logs.get("learning_rate")
        if loss is not None:
            logger.info(f"Step {step:>6} | loss={loss:.4f} | lr={lr:.2e}")


class BestModelCallback(TrainerCallback):
    """Log when a new best model checkpoint is saved."""

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        logger.info(
            f"Checkpoint saved at step {state.global_step} → {args.output_dir}"
        )
