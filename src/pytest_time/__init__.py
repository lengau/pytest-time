"""Pytest plugin for manipulating the time."""
import pytest

from pytest_time.instant_sleep import instant_sleep, InstantSleep

__all__ = ["instant_sleep", "mock_instant_sleep"]

from pytest_time.mock_time import MockWrapper


@pytest.fixture()
def mock_instant_sleep(
    monkeypatch: pytest.MonkeyPatch, instant_sleep: InstantSleep
) -> MockWrapper:
    """Get a mock wrapper that makes sleep occur instantly."""
    wrapper = MockWrapper(instant_sleep)
    wrapper.install(monkeypatch)
    return wrapper
