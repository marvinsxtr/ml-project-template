from hydra_zen import builds, store

from src.configs.logging.wandb import WandBConfig
from src.configs.runs.base import JobConfig, RunConfig, SweepConfig
from src.runs.main import main

main_config = builds(main, cfg=RunConfig, populate_full_signature=True)
store(main_config, name="root", hydra_defaults=["_self_", {"cfg/wandb": None}, {"cfg/job": None}])

wandb_store = store(group="cfg/wandb")
wandb_store(WandBConfig, name="base")

job_store = store(group="cfg/job")
job_store(JobConfig, name="base")
job_store(SweepConfig, name="sweep")
