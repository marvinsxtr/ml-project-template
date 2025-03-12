import logging
import os
import random
from pathlib import Path
from typing import Final

import numpy as np
import torch
from hydra.core.hydra_config import HydraConfig

logger = logging.getLogger()


class ConfigKeys:
    """Keys present in configs."""

    CONFIG: Final[str] = "cfg"
    SEED: Final[str] = "seed"
    WANDB: Final[str] = "wandb"
    JOB: Final[str] = "job"
    STORE: Final[str] = "store"


def seed_everything(seed: int) -> None:
    """Seeds all random number generators.

    Args:
        seed: Random seed.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def get_device() -> str:
    """Returns the available device for torch.

    Returns:
        The GPU or the MPS device when available and the CPU device as a fallback.
    """
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def get_hydra_output_dir() -> Path:
    """Return the hydra output directory.

    Returns:
        Path to the hydra output directory.
    """
    return Path(HydraConfig.get().runtime.output_dir)
