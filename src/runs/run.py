from dataclasses import dataclass

from src.common.logging.wandb import WandBRun
from src.runs.job import Job


@dataclass
class Run:
    """Configures a basic run."""

    seed: int
    wandb: WandBRun | None = None
    job: Job | None = None
