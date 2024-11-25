FROM --platform=$BUILDPLATFORM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 AS linux-base

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

# Google Cloud SDK
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-418.0.0-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh
ENV PATH=$PATH:/usr/local/gcloud/google-cloud-sdk/bin

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
