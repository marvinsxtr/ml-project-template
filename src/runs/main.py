from src.common.logging.logger import logger
from src.common.utils.config import run
from src.runs.run import Run


def main(cfg: Run, foo: int = 42, bar: int = 3) -> None:
    """Run a main function from a config.

    Args:
    ----
        cfg: Run config.
        foo: Some parameter.
        bar: Another parameter.
    """
    logger.info(f"Hello World! cfg={cfg}, bar={bar}, foo={foo}")


if __name__ == "__main__":
    import src.configs.stores.main  # noqa: F401

    run(main)
