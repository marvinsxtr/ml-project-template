from ml_project_template.config import run
from ml_project_template.runs import Run
from ml_project_template.utils import logger


def main(cfg: Run, foo: int = 42, bar: int = 3) -> None:
    """Run a main function from a config.

    Args:
        cfg: Run config.
        foo: Some parameter.
        bar: Another parameter.
    """
    logger.info(f"Hello World! cfg={cfg}, bar={bar}, foo={foo}")


if __name__ == "__main__":
    from example import stores  # noqa: F401

    run(main)
