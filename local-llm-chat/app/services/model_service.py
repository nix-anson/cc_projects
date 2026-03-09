"""HuggingFace model loading and streaming generation service."""
from __future__ import annotations

import asyncio
import logging
import threading
from typing import AsyncIterator

from app.core.config import settings
from app.core.gpu_utils import recommended_device

logger = logging.getLogger(__name__)


class ModelService:
    """Loads a HuggingFace model once and exposes async streaming generation."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = recommended_device()
        self._loaded = False
        self._model_id: str = ""

    # ─── Loading ──────────────────────────────────────────────────────────────

    def load(self, model_id: str | None = None, lora_adapter_path: str | None = None) -> None:
        """Load model + tokenizer (blocking — call from lifespan startup)."""
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        import torch

        model_id = model_id or settings.base_model_id
        lora_adapter_path = lora_adapter_path or settings.lora_adapter_path or None

        logger.info(f"Loading tokenizer: {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True,
            token=settings.hf_token or None,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # 4-bit quantization when CUDA is available
        quant_config = None
        if self.device == "cuda":
            try:
                quant_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                )
                logger.info("Using 4-bit QLoRA quantization")
            except Exception as e:
                logger.warning(f"bitsandbytes unavailable, loading in fp16: {e}")

        logger.info(f"Loading model: {model_id} on {self.device}")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quant_config,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
            token=settings.hf_token or None,
        )
        if self.device != "cuda":
            self.model = self.model.to(self.device)

        # Load LoRA adapter if specified
        if lora_adapter_path:
            self._load_lora(lora_adapter_path)

        self.model.eval()
        self._model_id = model_id
        self._loaded = True
        logger.info("Model ready.")

    def _load_lora(self, adapter_path: str) -> None:
        from peft import PeftModel

        logger.info(f"Loading LoRA adapter: {adapter_path}")
        self.model = PeftModel.from_pretrained(self.model, adapter_path)

    def unload(self) -> None:
        """Release GPU memory."""
        import gc
        import torch

        self.model = None
        self.tokenizer = None
        self._loaded = False
        gc.collect()
        if self.device == "cuda":
            torch.cuda.empty_cache()
        logger.info("Model unloaded.")

    # ─── Inference ────────────────────────────────────────────────────────────

    def _build_prompt(self, message: str, history: list[dict] | None = None) -> str:
        """Format a chat message into the model's expected prompt format."""
        parts = []
        for turn in (history or []):
            role = turn.get("role", "user")
            content = turn.get("content", "")
            parts.append(f"<|{role}|>\n{content}")
        parts.append(f"<|user|>\n{message}")
        parts.append("<|assistant|>")
        return "\n".join(parts)

    async def stream_generate(
        self,
        message: str,
        history: list[dict] | None = None,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        repetition_penalty: float | None = None,
    ) -> AsyncIterator[str]:
        """Async generator that yields tokens as they are produced."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        from transformers import TextIteratorStreamer

        prompt = self._build_prompt(message, history)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )

        gen_kwargs = {
            **inputs,
            "streamer": streamer,
            "max_new_tokens": max_new_tokens or settings.max_new_tokens,
            "temperature": temperature or settings.temperature,
            "top_p": top_p or settings.top_p,
            "repetition_penalty": repetition_penalty or settings.repetition_penalty,
            "do_sample": True,
        }

        queue: asyncio.Queue[str | None] = asyncio.Queue()
        loop = asyncio.get_event_loop()

        def _generate_in_thread():
            try:
                self.model.generate(**gen_kwargs)
            finally:
                # Signal completion
                loop.call_soon_threadsafe(queue.put_nowait, None)

        def _stream_to_queue():
            for token_text in streamer:
                loop.call_soon_threadsafe(queue.put_nowait, token_text)

        # Run generation in background thread; concurrently drain streamer
        gen_thread = threading.Thread(target=_generate_in_thread, daemon=True)
        stream_thread = threading.Thread(target=_stream_to_queue, daemon=True)
        gen_thread.start()
        stream_thread.start()

        while True:
            token = await queue.get()
            if token is None:
                break
            if token:
                yield token


# Singleton — loaded once per server process via lifespan
model_service = ModelService()
