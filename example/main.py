from example.configs import Run
from ml_project_template.config import run
from ml_project_template.utils import basic_seed_fn, logger


def main(cfg: Run) -> None:
    """Run a main function from a config.

    Args:
        cfg: Run config.
    """
    logger.info(f"Hello World! foo={cfg.foo}, bar={cfg.bar}")


if __name__ == "__main__":
    from example import stores  # noqa: F401

    run(main, seed_fn=basic_seed_fn)
