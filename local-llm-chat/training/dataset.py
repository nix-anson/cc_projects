"""Dataset loading and instruction-format preprocessing."""
from __future__ import annotations

from training.config import TrainingConfig


def load_dataset(cfg: TrainingConfig):
    """Load a HuggingFace dataset or local JSON/CSV file."""
    from datasets import load_dataset as hf_load_dataset

    if cfg.dataset_path:
        # Local file: infer format from extension
        path = cfg.dataset_path
        if path.endswith(".json") or path.endswith(".jsonl"):
            dataset = hf_load_dataset("json", data_files=path, split=cfg.dataset_split)
        elif path.endswith(".csv"):
            dataset = hf_load_dataset("csv", data_files=path, split=cfg.dataset_split)
        else:
            raise ValueError(f"Unsupported local dataset format: {path}")
    elif cfg.dataset_name:
        dataset = hf_load_dataset(
            cfg.dataset_name,
            split=cfg.dataset_split,
            token=cfg.hf_token or None,
        )
    else:
        raise ValueError("Either dataset_name or dataset_path must be set in config.")

    return dataset


def format_instruction(example: dict, text_column: str = "text") -> dict:
    """
    Convert a dataset example to instruction-tuning format.

    Expects either:
      - A single 'text' column (already formatted)
      - 'instruction' + optional 'input' + 'output' columns (Alpaca format)
    """
    if text_column in example:
        return {text_column: example[text_column]}

    instruction = example.get("instruction", "")
    context = example.get("input", "")
    response = example.get("output", "")

    if context:
        text = (
            f"<|user|>\n{instruction}\n\nContext: {context}\n<|assistant|>\n{response}"
        )
    else:
        text = f"<|user|>\n{instruction}\n<|assistant|>\n{response}"

    return {text_column: text}


def prepare_dataset(cfg: TrainingConfig):
    """Load, format, and return dataset ready for SFTTrainer."""
    dataset = load_dataset(cfg)

    # Only format if the text column is not already present
    if cfg.text_column not in dataset.column_names:
        dataset = dataset.map(
            lambda ex: format_instruction(ex, cfg.text_column),
            remove_columns=dataset.column_names,
        )

    return dataset
