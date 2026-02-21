from typing import NamedTuple

from hydra_zen import builds

from ml_project_template.runs import Job, SlurmParams, SweepJob
from ml_project_template.wandb import WandBRun


class Run(NamedTuple):
    """Configures a basic run."""

    seed: int | None = None
    wandb: WandBRun | None = None
    job: Job | None = None
    commit: str | None = None


RunConfig = builds(Run, commit=None)

SlurmParamsConfig = builds(
    SlurmParams,
    partition="cpu-2h",
    time_hours=2,
    cpus_per_task=2,
    gpus_per_task=0,
    mem_gb=8,
    nodes=1,
    tasks_per_node=1,
)

JobConfig = builds(Job, image="oras://ghcr.io/marvinsxtr/causal-fm:latest-sif", slurm_params=SlurmParamsConfig)

SweepConfig = builds(SweepJob, num_workers=2, parameters={"foo": [42, 1337]}, builds_bases=(JobConfig,))

WandBConfig = builds(WandBRun, group=None, mode="online")
