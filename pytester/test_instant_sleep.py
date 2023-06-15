"""Pytester test for InstantSleep."""
from __future__ import annotations

import time
from typing import TYPE_CHECKING
from unittest import mock

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable


def snooze(ms: int | float) -> None:
    """Sleep for a certain number of milliseconds."""
    time.sleep(ms / 1000)


@pytest.fixture()
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
