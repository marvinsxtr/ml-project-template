import pytest
from hydra_zen import instantiate, launch
from omegaconf import DictConfig

from example.stores import MainConfig


def wrap(config: DictConfig) -> None:
    """Instantiates a given config."""
    instantiate(config)


def test_example_config(capsys: pytest.CaptureFixture[str]) -> None:
    """Test main config."""
    launch(MainConfig, task_function=wrap, version_base=None, overrides=["foo=123"])
    captured = capsys.readouterr()
    assert "foo=123" in captured.out
