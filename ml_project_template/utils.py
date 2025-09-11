import logging
import os
import random
from pathlib import Path
from typing import Final

from hydra.core.hydra_config import HydraConfig

logger = logging.getLogger()


class ConfigKeys:
    """Keys present in configs."""

    CONFIG: Final[str] = "cfg"
    SEED: Final[str] = "seed"
    WANDB: Final[str] = "wandb"
    JOB: Final[str] = "job"
    STORE: Final[str] = "store"


def basic_seed_fn(seed: int) -> None:
    """Seeds random number generators.

    Args:
        seed: Random seed.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def get_output_dir() -> Path:
    """Get the current output directory.

    Returns:
    Output path of the current run.
    """
    try:
        output_dir = Path(HydraConfig.get().runtime.output_dir)
    except ValueError:
        output_dir = Path("/tmp/outputs")
        output_dir.mkdir(exist_ok=True, parents=True)
    return output_dir
