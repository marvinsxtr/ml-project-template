# ML Project Template

This is a template project for ML experimentation using wandb, hydra-zen, submitit on a Slurm cluster using Docker and Apptainer for containerization.

**NOTE**: This template is optimized for the specific setup of the ML Group cluster but may be easily adapted to similar settings.

## Highlights

* Python environment in Docker via [uv](https://docs.astral.sh/uv/)
* Logging and visualizations via [Weights and Biases](https://wandb.com)
* Reproducibility and modular type-checked configs via [hydra-zen](https://github.com/mit-ll-responsible-ai/hydra-zen)
* Submit Slurm jobs and sweeps directly from Python via [submitit](https://github.com/facebookincubator/submitit)
* No `.def` or `.sh` files needed for Apptainer/Slurm

## Setup

To be able to run Slurm from within Apptainer, you first have to add the following lines to your `.zshrc`/`.bashrc` file:

```bash
export APPTAINER_BIND=/opt/slurm-23.2,/opt/slurm,/etc/slurm,/etc/munge,/var/log/munge,/var/run/munge,/lib/x86_64-linux-gnu
export APPTAINERENV_APPEND_PATH=/opt/slurm/bin:/opt/slurm/sbin
```

You can then use the given `Dockerfile` to start a shell via 

```bash
apptainer shell docker://ghcr.io/marvinsxtr/ml-project-template:main
```

Note: This may take a few minutes on the first run.

You can replace `main` with a version tag, e.g. `latest`or `v0.0.1`.

To use version tags for indexing Dockerimage versions use the follwing after commiting the Dockerimage:

```bash
git tag v0.0.1
git push
git push origin tag v0.0.1
```

### WandB Logging

Logging to WandB is optional for running local jobs but mandatory for jobs submitted to the cluster.

WandB is enabled by specifying an API key, the project and entity in a `.env` file in the root of the repository. You can take the following snippet as a template:

```bash
WANDB_API_KEY=
WANDB_ENTITY=
WANDB_PROJECT=
```

### Local

You can run a script locally via

```bash
python src/ml_project_template/runs/main.py
```

Hydra should automatically generate a `config.yaml` in the `outputs/<date>/<time>/.hydra` folder which you can use to reproduce the same run later. Using the command line arguments, you can override or switch out parts of this config as you will see in the following sections.

To log to WandB, add `cfg/wandb=base`:

```bash
python src/ml_project_template/runs/main.py cfg/wandb=base
```

In order to use WandB in offline mode, add `cfg.wandb.mode=offline`:

```bash
python src/ml_project_template/runs/main.py cfg/wandb=base cfg.wandb.mode=offline
```

### Single Job

To run the command as a job in the cluster, run

```bash
python src/ml_project_template/runs/main.py cfg/job=base
```

This will automatically add WandB logging for you. See `src/ml_project_template/configs/runs/base.py` to configure the job to your needs.

### Distributed Sweep

Run a sweep over two seeds using multiple nodes:

```bash
python src/ml_project_template/runs/main.py cfg/job=sweep
```

This will automatically add WandB logging for you. See `src/ml_project_template/configs/runs/base.py` to configure the sweep to your needs.

## Docker Image

The Docker image can be built for `linux/amd64` by running

```bash
docker buildx build -t ml-project-template .
```

When using VSCode, the Docker image is automatically built when using a Dev Container.

## Acknowledgements

This template is based on a [previous example project](https://github.com/mx-e/example_project_ml_cluster).