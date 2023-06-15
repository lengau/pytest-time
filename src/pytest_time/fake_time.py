"""Base class for faking time."""
from __future__ import annotations

import abc
import time
import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def _ns_to_sec(ns: int) -> float:
    """Convert nanoseconds to seconds."""
    return float(ns) * 0.000_000_001


class FakeTime(metaclass=abc.ABCMeta):
    """Abstract base class for fake times."""

    def __init__(self) -> None:
        self._time = types.SimpleNamespace()

    def sleep(self, secs: float | int) -> None:  # noqa: ARG002
        # Ignore the unused `secs` argument.
        """Sleep like time.sleep, but without really sleeping."""
        return

    @abc.abstractmethod
    def time_ns(self) -> int:
        """Get the time like time.time_ns."""

    def time(self) -> float:
        """Get the time like time.time.

        This default implementation uses this class's time_ns()
        """
        return _ns_to_sec(self.time_ns())

    @abc.abstractmethod
    def monotonic_ns(self) -> int:
        """Get the time like time.monotonic_ns."""

    def monotonic(self) -> float:
        """Get the time like time.monotonic.

        This default implementation uses this class's monotonic_ns()
        """
        return _ns_to_sec(self.monotonic_ns())

    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Install this fake timer into time using monkeypatch."""
        self._time.sleep = time.sleep
        monkeypatch.setattr("time.sleep", self.sleep)
        self._time.time_ns = time.time_ns
        monkeypatch.setattr("time.time_ns", self.time_ns)
        self._time.time = time.time
        monkeypatch.setattr("time.time", self.time)
        self._time.monotonic_ns = time.monotonic_ns
        monkeypatch.setattr("time.monotonic_ns", self.monotonic_ns)
        self._time.monotonic = time.monotonic
        monkeypatch.setattr("time.monotonic", self.monotonic)
