FROM --platform=linux/amd64 python:3.12-slim AS linux-base

# Utilities
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends build-essential \
    sudo curl git htop less rsync screen vim nano wget ca-certificates \
    openssh-client zsh

# Download and install VS Code Server CLI
RUN wget -O /tmp/vscode-server-cli.tar.gz "https://update.code.visualstudio.com/latest/cli-linux-x64/stable" && \
    mkdir -p /usr/local/bin && \
    tar -xf /tmp/vscode-server-cli.tar.gz -C /usr/local/bin && \
    rm /tmp/vscode-server-cli.tar.gz

# Slurm
RUN COMMANDS="sacct sacctmgr salloc sattach sbatch sbcast scancel scontrol sdiag sgather sinfo smap sprio squeue sreport srun sshare sstat strigger sview" \
    && for CMD in $COMMANDS; do echo '#!/bin/bash' > "/usr/local/bin/$CMD" \
    && echo 'ssh $USER@$SLURM_CLUSTER_NAME -t "cd $PWD; . ~/.zshrc 2>/dev/null || . ~/.bashrc 2>/dev/null; bash -lc '\'$CMD \$@\''"' >> "/usr/local/bin/$CMD" \
    && chmod +x "/usr/local/bin/$CMD"; done

FROM linux-base AS python-base

# Workdir
WORKDIR /srv/repo

# Environment variables
ENV UV_PROJECT_ENVIRONMENT="/venv"
ENV UV_PYTHON_INSTALL_DIR="/python"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON=python3.12
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"
ENV PYTHONPATH="/srv/repo:$PYTHONPATH"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /usr/local/bin/uv

# Environment
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
