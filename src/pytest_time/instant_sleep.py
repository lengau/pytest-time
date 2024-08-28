"""A pytest fixture for making time.sleep instant with proper side effects."""
from __future__ import annotations

from typing import cast

import pytest

from pytest_time import fake_time


class InstantSleep(fake_time.FakeTime):
    """A time faker that makes sleep instant, adjusting time values accordingly.

    This uses the real system clock, but adjusts the values from `time` after
    each `sleep` call.
    """

    def __init__(self) -> None:
        super().__init__()
        self.offset_ns = 0

    def sleep(self, secs: float) -> None:
        """Fake sleeping by adjusting a time offset."""
        if secs < 0:
            return
        self.offset_ns += round(secs * 1_000_000_000)

    def time_ns(self) -> int:
        """Get time.time_ns."""
        return cast(int, self._time.time_ns() + self.offset_ns)

    def monotonic_ns(self) -> int:
        """Get time.monotonic_ns."""
        return cast(int, self._time.monotonic_ns() + self.offset_ns)


@pytest.fixture
def instant_sleep(monkeypatch: pytest.MonkeyPatch) -> InstantSleep:
    """Fixture for speeding through time.sleep."""
    sleep = InstantSleep()
    sleep.install(monkeypatch)
    return sleep
