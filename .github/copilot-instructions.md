# Copilot Instructions — ML Project Template

## Architecture

This is a **library + example** repo. The reusable library lives in `ml_project_template/` and a reference project using it lives in `example/`.

### Core library (`ml_project_template/`)

| Module | Purpose |
|--------|---------|
| `config.py` | `run()` entry point — wires hydra-zen `zen()` with a `pre_call` hook that handles seeding, WandB init, and config saving |
| `runs.py` | Dataclasses `Job` and `SweepJob` for submitting Slurm jobs via submitit |
| `wandb.py` | `WandBRun` (init from `.env`), `WandBConfig`, and `register_sweep()` |
| `utils.py` | `ConfigKeys` constants, `basic_seed_fn`, `get_output_dir()`, `git_commit_hash()`, logging |

### How a new experiment is wired (data flow)

1. **Define a `Run` config** as a `NamedTuple` in `example/configs.py` with optional fields `seed`, `wandb`, `job`, `commit`.
2. **Create hydra-zen `builds()` configs** for `Run`, `Job`, `SweepJob`, `WandBRun`, and `SlurmParams` in `configs.py`.
3. **Register configs into the hydra store** in `example/stores.py` using `store()` with named groups (`cfg`, `cfg/wandb`, `cfg/job`). The root `MainConfig` uses `builds(main, cfg=MISSING, populate_full_signature=True)` to expose `main`'s extra parameters (e.g. `foo`, `bar`) as top-level config keys.
4. **Write a `main(cfg: Run, ...)` function** in `example/main.py` with hyperparams as additional keyword arguments (not inside `Run`). Import stores at `__main__` time, then call `run(main, seed_fn=basic_seed_fn)`.
5. `run()` in `config.py` calls `store.add_to_hydra_store()` and launches `zen(...).hydra_main()`.

## Key conventions

- **Config composition**: configs use hydra-zen `builds()`, NOT yaml files. Hydra yaml is auto-generated in `outputs/<date>/<time>/.hydra/`.
- **Store imports at `__main__`**: stores are imported inside `if __name__ == "__main__"` to avoid side-effects during testing (see `example/main.py`).
- **`ConfigKeys` constants**: always reference config keys via `ConfigKeys.CONFIG` (`"cfg"`), `ConfigKeys.SEED`, etc. — never use raw strings.
- **`Run` is a `NamedTuple`**: experiment configs use `NamedTuple`, not `dataclass`, for hydra-zen compatibility. `Run` holds only structural fields (`seed`, `wandb`, `job`, `commit`); hyperparams go as extra args on `main()`.
- **CLI overrides**: hyperparams that are direct `main()` args use top-level keys (`foo=123`). Fields inside `Run` use the `cfg.` prefix (`cfg.seed=42`). Store groups use slash syntax (`cfg/wandb=base`, `cfg/job=sweep`).
- **WandB credentials**: loaded from a `.env` file at repo root (`WANDB_API_KEY`, `WANDB_ENTITY`, `WANDB_PROJECT`).

## Commands

```bash
# Run example locally
python example/main.py

# Override config values
python example/main.py foo=123

# Enable WandB logging
python example/main.py cfg/wandb=base

# Submit single Slurm job
python example/main.py cfg/job=base

# Submit parameter sweep
python example/main.py cfg/job=sweep

# Run tests
pytest

# Lint
ruff check .
ruff format --check .
```

## Testing pattern

Tests instantiate configs directly with `hydra_zen.launch()` — see `example/tests/test_example.py`. No live WandB or Slurm needed. Use `launch(MainConfig(cfg=RunConfig), task_function=wrap, version_base=None, overrides=[...])` to test config instantiation.

## Code style

- **Ruff** with `select = ["ALL"]` and specific ignores (see `pyproject.toml`). Line length 119.
- Google-style docstrings (`tool.ruff.pydocstyle` convention).
- Type annotations required on all public functions (Python 3.12+ syntax: `X | None`, not `Optional[X]`).
- `assert` is allowed in tests (`S101` ignored for `**/tests/**`).
