from hydra_zen import builds

from src.common.logging.wandb import WandBRun

WandBConfig = builds(WandBRun, group=None, mode="online")
