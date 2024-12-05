import os
import random

import numpy as np
import torch


def seed_everything(seed: int) -> None:
    """Seeds all random number generators.

    Args:
    ----
        seed: Random seed.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def get_device() -> str:
    """Returns the available device for torch.

    Returns
    -------
    The GPU or the MPS device when available and the CPU device as a fallback.
    """
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"
