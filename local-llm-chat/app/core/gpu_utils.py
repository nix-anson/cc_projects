"""CUDA / MPS / CPU detection and VRAM reporting."""
from __future__ import annotations
import sys
from typing import Any


def get_device_info() -> dict[str, Any]:
    """Return a dictionary describing available compute devices."""
    info: dict[str, Any] = {
        "python_version": sys.version,
        "device": "cpu",
        "cuda_available": False,
        "mps_available": False,
        "gpu_count": 0,
        "gpus": [],
    }

    try:
        import torch

        info["torch_version"] = torch.__version__

        if torch.cuda.is_available():
            info["cuda_available"] = True
            info["device"] = "cuda"
            gpu_count = torch.cuda.device_count()
            info["gpu_count"] = gpu_count
            for i in range(gpu_count):
                props = torch.cuda.get_device_properties(i)
                total_vram = props.total_memory / (1024 ** 3)
                allocated = torch.cuda.memory_allocated(i) / (1024 ** 3)
                reserved = torch.cuda.memory_reserved(i) / (1024 ** 3)
                info["gpus"].append(
                    {
                        "index": i,
                        "name": props.name,
                        "total_vram_gb": round(total_vram, 2),
                        "allocated_gb": round(allocated, 2),
                        "reserved_gb": round(reserved, 2),
                        "free_gb": round(total_vram - reserved, 2),
                        "compute_capability": f"{props.major}.{props.minor}",
                    }
                )

        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            info["mps_available"] = True
            info["device"] = "mps"

    except ImportError:
        info["torch_version"] = "not installed"

    return info


def recommended_device() -> str:
    """Return the best available device string for torch."""
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"
