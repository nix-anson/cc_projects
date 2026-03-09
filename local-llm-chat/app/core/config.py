"""Application settings loaded from environment / .env file."""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Model
    base_model_id: str = "microsoft/phi-2"
    lora_adapter_path: str = ""

    # Generation defaults
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    repetition_penalty: float = 1.1

    # HuggingFace
    hf_token: str = ""

    # Training output
    output_dir: str = "models/adapters"
    logging_dir: str = "logs"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
