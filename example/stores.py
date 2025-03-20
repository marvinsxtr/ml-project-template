from hydra_zen import builds, store

from example.configs import JobConfig, RunConfig, SweepConfig, WandBConfig
from example.main import main

MainConfig = builds(main, cfg=RunConfig, populate_full_signature=True)
store(MainConfig, name="root", hydra_defaults=["_self_", {"cfg/wandb": None}, {"cfg/job": None}])

wandb_store = store(group="cfg/wandb")
wandb_store(WandBConfig, name="base")

job_store = store(group="cfg/job")
job_store(JobConfig, name="base")
job_store(SweepConfig, name="sweep")
