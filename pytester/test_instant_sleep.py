"""Pytester test for InstantSleep."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING
from unittest import mock

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable


def snooze(ms: float) -> None:
    """Sleep for a certain number of milliseconds."""
    time.sleep(ms / 1000)


@pytest.fixture
def mock_sleep(monkeypatch: pytest.MonkeyPatch) -> Callable[[float], None]:
    """Get a mock object that wraps time.sleep."""
    sleep = mock.Mock(wraps=time.sleep)
    monkeypatch.setattr("time.sleep", sleep)
    return sleep


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("ms", [0, 1, 10, 100, 1000, 1_000_000])
def test_snooze(ms: int) -> None:
    """Test that snooze works."""
    snooze(ms)


@pytest.mark.usefixtures("instant_sleep")
@pytest.mark.parametrize("ms", [0, 1, 10, 100, 1000, 1_000_000])
def test_snooze_with_mock_sleep(ms: int, mock_sleep: mock.Mock) -> None:
    """Tests that snooze works even when I mock out sleep."""
    snooze(ms)

    mock_sleep.assert_called_once_with(ms * 0.001)


@pytest.mark.parametrize("sleep_time", [1, 10, 100])
@pytest.mark.usefixtures("instant_sleep")
def test_instant_sleep(sleep_time) -> None:
    start_time = time.time()
    start_monotonic = time.monotonic()

    time.sleep(sleep_time)

    # Subtract 1 microsecond from sleep time for floating point issues.
    assert time.time() >= start_time + (sleep_time - 0.000_000_1)
    assert time.monotonic() >= start_monotonic + (sleep_time - 0.000_000_1)
