import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml
from submitit import AutoExecutor
from submitit.helpers import CommandFunction

from src.common.logging.logger import get_hydra_output_dir, logger
from src.common.logging.wandb import WandBConfig
from src.common.utils.constants import ConfigKeys


@dataclass
class Job:
    """Job to run code on a cluster using apptainer."""

    image: str
    partition: str
    cluster: str
    kwargs: dict

    def __post_init__(self) -> None:
        """Run the job and exit."""
        self.run()
        sys.exit(0)

    def filter_args(self, args: list[str]) -> list[str]:
        """Filter args to prevent recursive jobs on the cluster."""
        return [arg for arg in args if f"{ConfigKeys.CONFIG}/{ConfigKeys.JOB}" not in arg]

    @property
    def python_command(self) -> str:
        """Python command used by the job."""
        return f"apptainer exec {self.image} python"

    def run(self) -> None:
        """Run the job on the cluster."""
        command = ["python", *self.filter_args(sys.argv), "cfg/wandb=base"]

        function = CommandFunction(command)
        executor = AutoExecutor(
            folder=get_hydra_output_dir(),
            cluster=self.cluster,
            slurm_python=self.python_command,
        )
        executor.update_parameters(**self.kwargs)
        job = executor.submit(function)

        logger.info(f"Submitted job {job.job_id}")


@dataclass
class SweepJob(Job):
    """Job to run a sweep on a cluster."""

    num_workers: int
    parameters: dict[str, list[Any]]
    metric_name: str = "loss"
    metric_goal: Literal["maximize", "minimize"] = "minimize"

    def register_sweep(self, sweep_config: dict) -> str:
        """Register a wandb sweep from a config."""
        if (wandb_config := WandBConfig.from_env()) is None:
            raise RuntimeError("No WandB config found in environment.")

        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "sweep_config.yaml"

            with Path.open(config_path, "w") as config_file:
                yaml.dump(sweep_config, config_file)

            output = subprocess.run(
                ["wandb", "sweep", "--project", wandb_config.WANDB_PROJECT, str(config_path)],
                check=True,
                text=True,
                capture_output=True,
            ).stderr

            sweep_id = output.split(" ")[-1].strip()

            for line in output.splitlines():
                logger.info(line)

        return sweep_id

    def run(self) -> None:
        """Run the sweep on the cluster."""
        parameters = {cfg_key: {"values": list(values)} for cfg_key, values in self.parameters.items()}
        metric = {"goal": self.metric_goal, "name": self.metric_name}
        program, args = sys.argv[0], self.filter_args(sys.argv[1:])
        command = ["${env}", "${interpreter}", "${program}", *args, "cfg/wandb=base", "${args_no_hyphens}"]

        sweep_config = {
            "program": program,
            "method": "grid",
            "metric": metric,
            "parameters": parameters,
            "command": command,
        }

        sweep_id = self.register_sweep(sweep_config)

        function = CommandFunction(["wandb", "agent"])
        executor = AutoExecutor(
            folder=get_hydra_output_dir(),
            cluster=self.cluster,
            slurm_python=self.python_command,
        )
        executor.update_parameters(
            slurm_array_parallelism=self.num_workers,
            **self.kwargs,
        )
        jobs = executor.map_array(function, [sweep_id] * self.num_workers)

        for job in jobs:
            logger.info(f"Submitted job {job.job_id}")
