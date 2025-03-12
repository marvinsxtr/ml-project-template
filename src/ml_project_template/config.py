import logging
from collections.abc import Callable
from functools import partial

import wandb
from hydra_zen import instantiate, store, to_yaml, zen
from hydra_zen.third_party.pydantic import pydantic_parser
from omegaconf import DictConfig, OmegaConf

from ml_project_template.utils import ConfigKeys, get_hydra_output_dir, logger, seed_everything
from ml_project_template.wandb import WandBRun


def pre_call(root_config: DictConfig, log_debug: bool = False) -> None:
    """Logs the config, sets the seed and initializes a WandB run before config instantiation.

    Args:
        root_config: Unresolved config.
        log_debug: Whether to log the config, seed and output path.
    """
    if log_debug:
        logger.setLevel(logging.DEBUG)

    config: DictConfig = root_config[ConfigKeys.CONFIG]

    if config.get(ConfigKeys.JOB, None) is not None:
        return

    if (seed := config.get(ConfigKeys.SEED)) is not None:
        seed_everything(seed)
        logger.debug(f"Set seed to {seed}.")
    else:
        logger.warning("No seed was configured! Run may not be reproducible.")

    if config is None:
        raise KeyError(f"Config must contain {ConfigKeys.CONFIG} at root-level.")
    else:
        logger.debug(f"Running config:\n{to_yaml(root_config)}")

    output_path = get_hydra_output_dir()
    logger.debug(f"Saving outputs in {output_path}")

    logger.setLevel(logging.INFO)

    if (wandb_config := config.get(ConfigKeys.WANDB)) is not None:
        wandb_run: WandBRun = instantiate(wandb_config)
        wandb_run.run.config.update(OmegaConf.to_container(root_config))
        wandb.save(output_path / ".hydra/*", base_path=output_path, policy="now")


def run(main_function: Callable, log_debug: bool = True) -> None:
    """Configure and run a given function using hydra-zen.

    Args:
        main_function: Function to configure and run.
        log_debug: Whether to log debug information from the `pre_call` function.
    """
    store.add_to_hydra_store()
    zen(
        main_function,
        pre_call=partial(pre_call, log_debug=log_debug),
        resolve_pre_call=False,
        instantiation_wrapper=pydantic_parser,
    ).hydra_main(
        config_name="root",
        config_path=None,
        version_base=None,
    )
