"""LoRA adapter management utilities."""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def merge_and_save(adapter_path: str, output_path: str) -> None:
    """
    Merge a LoRA adapter into the base model and save to disk.

    The merged model is a standard HuggingFace model that can be loaded
    without peft and pushed directly to the Hub.
    """
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    adapter_path = Path(adapter_path)
    output_path = Path(output_path)

    if not adapter_path.exists():
        raise FileNotFoundError(f"Adapter not found: {adapter_path}")

    # Read base model id from adapter config
    import json
    config_file = adapter_path / "adapter_config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"adapter_config.json not found in {adapter_path}")
    adapter_config = json.loads(config_file.read_text())
    base_model_name = adapter_config["base_model_name_or_path"]

    logger.info(f"Loading base model: {base_model_name}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True,
    )

    logger.info(f"Loading adapter: {adapter_path}")
    model = PeftModel.from_pretrained(base_model, str(adapter_path))

    logger.info("Merging weights...")
    merged = model.merge_and_unload()

    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving merged model to: {output_path}")
    merged.save_pretrained(str(output_path), safe_serialization=True)
    tokenizer.save_pretrained(str(output_path))
    logger.info("Merge complete.")


def push_adapter_to_hub(adapter_path: str, repo_id: str, token: str | None = None) -> None:
    """Upload a LoRA adapter directory to the HuggingFace Hub."""
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    logger.info(f"Uploading {adapter_path} -> hub:{repo_id}")
    api.create_repo(repo_id=repo_id, exist_ok=True, repo_type="model")
    api.upload_folder(
        folder_path=adapter_path,
        repo_id=repo_id,
        repo_type="model",
        commit_message="Upload LoRA adapter",
    )
    logger.info(f"Adapter pushed to: https://huggingface.co/{repo_id}")
