"""Training configuration dataclass loaded from YAML."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class LoRAConfig:
    r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: list[str] = field(default_factory=lambda: ["q_proj", "v_proj"])
    bias: str = "none"
    task_type: str = "CAUSAL_LM"


@dataclass
class QuantizationConfig:
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_compute_dtype: str = "bfloat16"


@dataclass
class TrainingConfig:
    # Model
    base_model_id: str = "microsoft/phi-2"
    hf_token: str = ""

    # Dataset
    dataset_name: str = ""          # HF dataset id, e.g. "timdettmers/openassistant-guanaco"
    dataset_path: str = ""          # OR local path under data/
    dataset_split: str = "train"
    max_seq_length: int = 1024
    text_column: str = "text"

    # Output
    output_dir: str = "models/adapters/run-001"
    logging_dir: str = "logs"

    # SFTTrainer args
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.05
    lr_scheduler_type: str = "cosine"
    save_steps: int = 100
    logging_steps: int = 10
    fp16: bool = False
    bf16: bool = True

    lora: LoRAConfig = field(default_factory=LoRAConfig)
    quantization: QuantizationConfig = field(default_factory=QuantizationConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "TrainingConfig":
        data = yaml.safe_load(Path(path).read_text())
        lora_data = data.pop("lora", {})
        quant_data = data.pop("quantization", {})
        cfg = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        if lora_data:
            cfg.lora = LoRAConfig(**lora_data)
        if quant_data:
            cfg.quantization = QuantizationConfig(**quant_data)
        return cfg
