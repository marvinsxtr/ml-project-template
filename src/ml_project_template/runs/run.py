from dataclasses import dataclass

from ml_project_template.common.logging.wandb import WandBRun
from ml_project_template.runs.job import Job


@dataclass
class Run:
    """Configures a basic run."""

    seed: int
    wandb: WandBRun | None = None
    job: Job | None = None
