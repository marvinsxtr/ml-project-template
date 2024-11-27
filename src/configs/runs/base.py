from hydra_zen import builds

from src.runs.job import Job, SweepJob
from src.runs.run import Run

RunConfig = builds(Run, seed=42, wandb=None, job=None)

JobConfig = builds(
    Job, partition="cpu-2h", image="docker://ghcr.io/marvinsxtr/ml-project-template:main", cluster="slurm", kwargs={}
)

SweepConfig = builds(SweepJob, num_workers=2, parameters={"cfg.seed": [42, 1337]}, builds_bases=(JobConfig,))
