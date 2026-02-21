from example.configs import Run
from ml_project_template.config import run
from ml_project_template.utils import basic_seed_fn, logger


def main(cfg: Run, foo: int = 42, bar: int = 3) -> None:
    """Run a main function from a config."""
    logger.info(f"Hello World! {cfg=}, {foo=}, {bar=}")


if __name__ == "__main__":
    from example import stores  # noqa: F401

    run(main, seed_fn=basic_seed_fn)
