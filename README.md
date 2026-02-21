# 🚀 ML Project Template

A modern template for machine learning experimentation using **wandb**, **hydra-zen**, and **submitit** on a Slurm cluster with Docker/Apptainer containerization.

> **Note**: This template is optimized for the ML Group cluster setup but can be easily adapted to similar environments.

<div align="center">

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Docker](https://img.shields.io/badge/Docker-Container-blue.svg)](https://www.docker.com/)
[![WandB](https://img.shields.io/badge/WandB-Logging-yellow.svg)](https://wandb.ai)
[![Hydra Zen](https://img.shields.io/badge/Hydra%20Zen-Config-green.svg)](https://github.com/mit-ll-responsible-ai/hydra-zen)
[![Submitit](https://img.shields.io/badge/Submitit-Jobs-orange.svg)](https://github.com/facebookincubator/submitit)

</div>

## ✨ Key Features

- 📦 Python environment in Docker via [uv](https://docs.astral.sh/uv/)
- 📊 Logging and visualizations via [Weights and Biases](https://wandb.com)
- 🧩 Reproducibility and modular type-checked configs via [hydra-zen](https://github.com/mit-ll-responsible-ai/hydra-zen)
- 🖥️ Submit Slurm jobs and parameter sweeps directly from Python via [submitit](https://github.com/facebookincubator/submitit)
- 🔄 No `.def` or `.sh` files needed for Apptainer/Slurm

## 📋 Table of Contents

- [🔑 Container Registry Authentication](#-container-registry-authentication)
- [🐳 Container Setup](#-container-setup)
  - [Option 1: Apptainer (Cluster)](#option-1-apptainer-cluster)
  - [Option 2: Docker (Local Machine)](#option-2-docker-local-machine)
- [📦 Package Management](#-package-management)
- [🛠️ Development Notes](#️-development-notes)
- [🧪 Running Experiments](#-running-experiments)
  - [WandB Logging](#wandb-logging)
  - [Example Project](#example-project)
  - [Single Job](#single-job)
  - [Distributed Sweep](#distributed-sweep)
- [👥 Contributions](#-contributions)
- [🙏 Acknowledgements](#-acknowledgements)

## 🔑 Container Registry Authentication

### Generate Token

1. Create a new GitHub token at [Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) with:
   - `read:packages` permission
   - `write:packages` permission

### Log In

With Apptainer:
```bash
apptainer remote login --username <your GitHub username> docker://ghcr.io
```

With Docker:
```bash
docker login ghcr.io -u <your GitHub username>
```

When prompted, enter your token as the password.

## 🐳 Container Setup

Choose one of the following methods to set up your environment:

### Option 1: Apptainer (Cluster)

1. **Install VSCode Remote Tunnels Extension**

   First, install the [Remote Tunnels](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server) extension in VSCode.

2. **Connect to compute resources**

   For CPU resources:
   ```bash
   srun --partition=cpu-2h --pty bash
   ```
   
   For GPU resources:
   ```bash
   srun --partition=gpu-2h --gpus-per-task=1 --pty bash
   ```

3. **Launch container**

   To open a tunnel to connect your local VSCode to the container on the cluster:
   ```bash
   apptainer run --nv --writable-tmpfs oras://ghcr.io/marvinsxtr/ml-project-template:latest-sif code tunnel
   ```

   > 💡 You can specify a version tag (e.g., `v0.0.1`) instead of `latest`. Available versions are listed at [GitHub Container Registry](https://github.com/marvinsxtr/ml-project-template/pkgs/container/ml-project-template).

   In VSCode press `Shift+Alt+P` (Windows/Linux) or `Shift+Cmd+P` (Mac), type "connect to tunnel", select GitHub and select your named node on the cluster. Your IDE is now connected to the cluster.

   To open a shell in the container on the cluster:
   ```bash
   apptainer run --nv --writable-tmpfs oras://ghcr.io/marvinsxtr/ml-project-template:latest-sif /bin/bash
   ```

   > 💡 This may take a few minutes on the first run as the container image is downloaded.

### Option 2: Docker (Local Machine)

1. **Install VSCode Dev Containers Extension**

   First, install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VSCode.

2. **Open the Repository in the Dev Container**

   Click the `Reopen in Container` button in the pop-up that appears once you open the repository in VSCode.

   Alternatively, open the command palette in VSCode by pressing `Shift+Alt+P` (Windows/Linux) or `Shift+Cmd+P` (Mac), and type `Dev Containers: Reopen in Container`.

### Using Slurm within Apptainer

In order to access Slurm with submitit from within the container, you first need to set up passwordless SSH to the login node.

On the cluster, create a new SSH key pair in case you don't have one yet

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

and add your public key to the `authorized_keys`:

```bash
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```

You can verify that this works by running

```bash
ssh $USER@$HOST exit
```

which should return without any prompt.

## 📦 Package Management

1. **Update dependencies**

   This project uses [uv](https://docs.astral.sh/uv/) for Python dependency management.

   Inside the container (!):
   ```bash
   # Add a specific package
   uv add <package-name>

   # Update all dependencies from pyproject.toml
   uv sync
   ```

2. **Commit changes** to the repository:

   Use tags for versioning:

   ```bash
   git add pyproject.toml uv.lock 
   git commit -m "Updated dependencies"
   git tag v0.0.1
   git push && git push --tags
   ```

3. **Use the updated image**:

   The GitHub Actions workflow automatically builds a new image when changes are pushed.

   With Apptainer:
   ```bash
   apptainer run --nv --writable-tmpfs oras://ghcr.io/marvinsxtr/ml-project-template:v0.0.1-sif /bin/bash
   ```

   With Docker:
   ```bash
   docker run -it --rm --platform=linux/amd64 ghcr.io/marvinsxtr/ml-project-template:v0.0.1 /bin/bash
   ```

## 🛠️ Development Notes

### Building Locally for Testing

Test your Dockerfile locally before pushing:

```bash
docker buildx build -t ml-project-template .
```

Run the container directly with:

```bash
docker run -it --rm --platform=linux/amd64 ml-project-template /bin/bash
```

## 🧪 Running Experiments

### WandB Logging

Logging to WandB is optional for local jobs but mandatory for jobs submitted to the cluster.

Create a `.env` file in the root of the repository with:

```bash
WANDB_API_KEY=your_api_key
WANDB_ENTITY=your_entity
WANDB_PROJECT=your_project_name
```

### Example Project

The folder `example` contains an example project which can serve as a starting point for ML experimentation. Configuring a function 
```python
from ml_project_template.utils import logger

def main(foo: int = 42, bar: int = 3) -> None:
    """Run a main function from a config."""
    logger.info(f"Hello World! cfg={cfg}, bar={bar}, foo={foo}")

if __name__ == "__main__":
    main()
```

is as easy as adding (1) a `Run` as the first argument, (2) importing the config stores and (3) wrapping the `main` function with `run`:

```python
from ml_project_template.config import run
from ml_project_template.runs import Run
from ml_project_template.utils import logger

def main(cfg: Run, foo: int = 42, bar: int = 3) -> None:
    """Run a main function from a config."""
    logger.info(f"Hello World! cfg={cfg}, bar={bar}, foo={foo}")

if __name__ == "__main__":
    from example import stores  # noqa: F401
    run(main)
```

You can try running this example with:

```bash
python example/main.py
```

Hydra will automatically generate a `config.yaml` in the `outputs/<date>/<time>/.hydra` folder which you can use to reproduce the same run later.

Try overriding the values passed to the `main` function and see how it changes the output (config):

```bash
python example/main.py foo=123
```

Reproduce the results of a previous run/config:

```bash
python example/main.py -cp outputs/<date>/<time>/.hydra -cn config.yaml
```

Enabling WandB logging:

```bash
python example/main.py cfg/wandb=base
```

Run WandB in offline mode:

```bash
python example/main.py cfg/wandb=base cfg.wandb.mode=offline
```

### Single Job

Run a job on the cluster:

```bash
python example/main.py cfg/job=base
```

This will automatically enable WandB logging. See `example/configs.py` to configure the job settings.

### Distributed Sweep

Run a parameter sweep over multiple seeds using multiple nodes:

```bash
python example/main.py cfg/job=sweep
```

This will automatically enable WandB logging. See `example/configs.py` to configure sweep parameters.

## 👥 Contributions

Contributions to this documentation and template are very welcome! Feel free to open a PR or reach out with suggestions.

## 🙏 Acknowledgements

This template is based on a [previous example project](https://github.com/mx-e/example_project_ml_cluster).
