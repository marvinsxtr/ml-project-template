import logging
from pathlib import Path

from hydra.core.hydra_config import HydraConfig

logger = logging.getLogger()


def get_hydra_output_dir() -> Path:
    """Return the hydra output directory.

    Returns
    -------
    Path to the hydra output directory.
    """
    return Path(HydraConfig.get().runtime.output_dir)
