# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ML experiment template using **hydra-zen** (config), **wandb** (logging), and **submitit** (Slurm jobs). Python 3.12, managed with **uv**.

## Commands

```bash
# Install dependencies
uv sync --all-extras --dev

# Run tests
uv run pytest

# Run a single test
uv run pytest example/tests/test_example.py::test_example_config

# Lint and format
ruff check .
ruff format --check .

# Auto-fix lint issues
ruff check . --fix

# Run the example experiment
python example/main.py
python example/main.py foo=123              # override hyperparams
python example/main.py cfg/wandb=base       # enable WandB
python example/main.py cfg/job=base         # submit Slurm job
python example/main.py cfg/job=sweep        # parameter sweep
```

## Submitting cluster jobs with `bin/slurm-agent`

For an agent (e.g. Claude Code), `bin/slurm-agent` submits a Slurm job in one command — no interactive container/devcontainer, and it works from a login node that has neither python nor apptainer. It checks the target commit out into a per-commit worktree, runs the hydra-zen submitter in the image on a short CPU allocation, and submitit sbatches the job.

```bash
IMAGE=oras://ghcr.io/<you>/<project>:latest-sif JOB=<cfg/job option> bin/slurm-agent example/main.py [overrides…]
```

- **Commit and push first.** It runs a committed, pushed SHA from `$REPO/.worktrees/<sha>`, so uncommitted edits do NOT run — it refuses a dirty tree unless you pass `REF=<branch|sha>`. Concurrent jobs on different commits therefore never clobber each other's code.
- **From a laptop**, add `HOST=<cluster>`: it ssh's in (login shell), fetches the commit, and submits there. `SLURM_BIN=<dir>` if slurm isn't on the login PATH; `REMOTE_REPO=<path>` if the checkout isn't at the same path as locally.
- **Outputs & wandb**: it sets `HYDRA_OUTPUT_DIR` so `get_output_dir()` (submitit logs, checkpoints, wandb) points at one per-run dir, and passes wandb creds as env vars (a worktree has no `.env`; keep the API key in `~/.netrc` or a `.env` in the main checkout).
- The launcher sets `JOB_REPO`/`JOB_IMAGE`, read by `Job.python_command` — nothing else in the project needs changing. See the script header for all knobs.

## Architecture

**Library** (`ml_project_template/`) + **Example** (`example/`):

- `ml_project_template/config.py` — `run()` entry point: wires hydra-zen `zen()` with `pre_call` hook (seeding, WandB init, config saving)
- `ml_project_template/runs.py` — `Job` and `SweepJob` dataclasses for Slurm submission via submitit
- `ml_project_template/wandb.py` — `WandBRun`, `WandBConfig`, `register_sweep()`
- `ml_project_template/utils.py` — `ConfigKeys` constants, `basic_seed_fn`, `get_output_dir()`, `git_commit_hash()`, logging

### Experiment wiring flow

1. Define a `Run` config as a `NamedTuple` in `example/configs.py` (fields: `seed`, `wandb`, `job`, `commit`)
2. Create hydra-zen `builds()` configs for `Run`, `Job`, `SweepJob`, `WandBRun`, `SlurmParams`
3. Register configs into hydra store in `example/stores.py` using `store()` with named groups (`cfg`, `cfg/wandb`, `cfg/job`)
4. Write `main(cfg: Run, ...)` with hyperparams as extra keyword args (not inside `Run`)
5. Import stores at `__main__` time, then call `run(main, seed_fn=basic_seed_fn)`

## Key Conventions

- **Configs use hydra-zen `builds()`**, not YAML files. Hydra YAML is auto-generated in `outputs/<date>/<time>/.hydra/`
- **Store imports at `__main__`**: stores are imported inside `if __name__ == "__main__"` to avoid side-effects during testing
- **`ConfigKeys` constants**: reference config keys via `ConfigKeys.CONFIG`, `ConfigKeys.SEED`, etc. — never raw strings
- **`Run` is a `NamedTuple`** (not dataclass) for hydra-zen compatibility. Hyperparams go as extra args on `main()`, not inside `Run`
- **CLI override syntax**: top-level keys for `main()` args (`foo=123`), `cfg.` prefix for `Run` fields (`cfg.seed=42`), slash for store groups (`cfg/wandb=base`)
- **WandB credentials**: loaded from `.env` at repo root (`WANDB_API_KEY`, `WANDB_ENTITY`, `WANDB_PROJECT`)

## Code Style

- **Ruff** with `select = ["ALL"]` and specific ignores (see `pyproject.toml`). Line length 119
- Google-style docstrings
- Type annotations on all public functions using Python 3.12+ syntax (`X | None`, not `Optional[X]`)
- `assert` allowed in tests (`S101` ignored for `**/tests/**`)
- Pre-commit hooks run ruff check (with `--fix`) and ruff format

## Testing Pattern

Tests use `hydra_zen.launch()` to instantiate configs without live WandB or Slurm. See `example/tests/test_example.py` for the pattern:
```python
launch(MainConfig(cfg=RunConfig), task_function=wrap, version_base=None, overrides=[...])
```
