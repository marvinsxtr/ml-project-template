from hydra_zen import builds

from ml_project_template.common.logging.wandb import WandBRun

WandBConfig = builds(WandBRun, group=None, mode="online")
