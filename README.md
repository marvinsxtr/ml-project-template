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

- [Container Setup](#-container-setup)
  - [Option 1: Apptainer](#option-1-apptainer)
  - [Option 2: Docker](#option-2-docker)
- [Package Management](#-package-management)
- [Updating the Docker Image](#-updating-the-docker-image)
- [Container Registry Authentication](#-container-registry-authentication)
- [Development Notes](#-development-notes)
- [Running Experiments](#-running-experiments)
  - [WandB Logging](#wandb-logging)
  - [Local Execution](#local-execution)
  - [Single Job](#single-job)
  - [Distributed Sweep](#distributed-sweep)
- [Contributions](#-contributions)
- [Acknowledgements](#-acknowledgements)

## 🐳 Container Setup

Choose one of the following methods to set up your environment:

### Option 1: Apptainer

1. **Configure environment bindings**

   Add to your `.zshrc` or `.bashrc`:
   
   ```bash
   export APPTAINER_BIND=/opt/slurm-23.2,/opt/slurm,/etc/slurm,/etc/munge,/var/log/munge,/var/run/munge,/lib/x86_64-linux-gnu
   export APPTAINERENV_APPEND_PATH=/opt/slurm/bin:/opt/slurm/sbin
   ```

2. **Install VSCode Command Line Interface (Optional)**

   This step is required if you plan to create a remote tunnel. First, install the [Remote Tunnels](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server) extension in VSCode.

3. **Connect to compute resources**

   For CPU resources:
   ```bash
   srun --partition=cpu-2h --pty bash
   ```
   
   For GPU resources:
   ```bash
   srun --partition=gpu-2h --gpus-per-task=1 --pty bash
   ```

4. **Launch container**

   To open a tunnel to connect you local VSCode to the container on the cluster:
   ```bash
   apptainer run --nv --writable-tmpfs oras://ghcr.io/marvinsxtr/ml-project-template:latest-sif code tunnel
   ```

   In VSCode press `Shift+Alt+P` (Windows/Linux) or `Shift+Cmd+P` (Mac), type connect to tunnel, select GitHub and select your named node on the cluster. Your IDE is now connected to the cluster.

   To open a shell in the container on the cluster:
   ```bash
   apptainer run --nv --writable-tmpfs oras://ghcr.io/marvinsxtr/ml-project-template:latest-sif /bin/bash
   ```

   > 💡 This may take a few minutes on the first run as the container image is downloaded.

### Option 2: Docker

Run the container directly with:

```bash
docker run -it --rm --platform=linux/amd64 ghcr.io/marvinsxtr/ml-project-template:latest /bin/bash
```

> 💡 You can specify a version tag (e.g., `v0.0.1`) instead of `latest`. Available versions are listed at [GitHub Container Registry](https://github.com/marvinsxtr/ml-project-template/pkgs/container/ml-project-template).

## 📦 Package Management

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency management.

### Adding or Updating Dependencies

Inside the container (e.g., [VSCode shell with Docker Container](https://code.visualstudio.com/docs/devcontainers/containers)):

```bash
# Add a specific package
uv add <package-name>

# Update all dependencies from pyproject.toml or requirements.txt
uv sync
```

## 🔄 Updating the Docker Image

1. **Update dependencies** using `uv` as described above

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

## 🛠️ Development Notes

### Building Locally for Testing

Test your Dockerfile locally before pushing:

```bash
docker buildx build -t ml-project-template .
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

### Local Execution

Run a script locally with:

```bash
python src/example/main.py
```

Hydra will automatically generate a `config.yaml` in the `outputs/<date>/<time>/.hydra` folder which you can use to reproduce the same run later.

To enable WandB logging:

```bash
python src/example/main.py cfg/wandb=base
```

For WandB offline mode:

```bash
python src/example/main.py cfg/wandb=base cfg.wandb.mode=offline
```

### Single Job

To run a job on the cluster:

```bash
python src/example/main.py cfg/job=base
```

This will automatically enable WandB logging. See `src/example/configs.py` to configure the job settings.

### Distributed Sweep

Run a parameter sweep over multiple seeds using multiple nodes:

```bash
python src/example/main.py cfg/job=sweep
```

This will automatically enable WandB logging. See `src/example/configs.py` to configure sweep parameters.

## 👥 Contributions

Contributions to this documentation and template are very welcome! Feel free to open a PR or reach out with suggestions.

## 🙏 Acknowledgements

This template is based on a [previous example project](https://github.com/mx-e/example_project_ml_cluster).
