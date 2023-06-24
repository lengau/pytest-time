"""Pytest plugin for manipulating the time."""
import time

import pytest

from pytest_time.instant_sleep import instant_sleep, InstantSleep

__all__ = [
    "InstantSleep",
    "instant_sleep",
    "MockWrapper",
    "mock_instant_sleep",
    "__version__",
]

from pytest_time.wrap_time import MockWrapper

try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("pytest_time")
    except PackageNotFoundError:
        __version__ = "dev"


@pytest.fixture()
def mock_time(monkeypatch: pytest.MonkeyPatch) -> MockWrapper:
    wrapper = MockWrapper(time)  # type: ignore[arg-type]
    wrapper.install(monkeypatch)
    return wrapper


@pytest.fixture()
def mock_instant_sleep(
    monkeypatch: pytest.MonkeyPatch, instant_sleep: InstantSleep
) -> MockWrapper:
    """Get a mock wrapper that makes sleep occur instantly."""
    wrapper = MockWrapper(instant_sleep)
    wrapper.install(monkeypatch)
    return wrapper
