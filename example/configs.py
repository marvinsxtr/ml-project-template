from hydra_zen import builds

from ml_project_template.runs import Job, Run, SlurmParams, SweepJob
from ml_project_template.wandb import WandBRun

RunConfig = builds(Run, seed=42, wandb=None, job=None)

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

JobConfig = builds(Job, slurm_params=SlurmParamsConfig)

SweepConfig = builds(SweepJob, num_workers=2, parameters={"cfg.seed": [42, 1337]}, builds_bases=(JobConfig,))

WandBConfig = builds(WandBRun, group=None, mode="online")
