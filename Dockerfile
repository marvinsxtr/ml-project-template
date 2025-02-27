FROM --platform=linux/amd64 nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 AS linux-base

# Environment variables
ENV UV_PROJECT_ENVIRONMENT="/venv"
ENV UV_PYTHON_INSTALL_DIR="/python"
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON=python3.12
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Clean up
RUN rm -f /etc/apt/sources.list.d/*.list

# Utilities
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends build-essential \
    sudo curl git htop less rsync screen vim nano wget

# Download and install VS Code Server CLI
RUN wget -O /tmp/vscode-server-cli.tar.gz "https://update.code.visualstudio.com/latest/cli-linux-x64/stable" && \
    mkdir -p /usr/local/bin && \
    tar -xf /tmp/vscode-server-cli.tar.gz -C /usr/local/bin && \
    rm /tmp/vscode-server-cli.tar.gz

# Slurm
RUN groupadd -g 12067 slurm
RUN useradd  -m -d /tmp -u 13504 -g slurm -s /bin/false slurm
RUN groupadd -g 119 munge
RUN useradd  -m -d /nonexistent -u 114 -g munge -s /usr/sbin/nologin munge

FROM linux-base AS python-base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.4@sha256:49934a7a2d0a2ddfda9ddb566d6ac2449cdf31c7ebfb56fe599e04057fddca58 /uv /usr/local/bin/uv

# Environment
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Workdir
RUN mkdir /srv/repo/ && chmod 777 /srv/repo
ENV PYTHONPATH=$PYTHONPATH:/srv/repo
WORKDIR /srv/repo
