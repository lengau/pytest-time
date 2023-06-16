"""A pytest fixture for mocking time calls to record them."""
from __future__ import annotations

from unittest import mock

import pytest

from pytest_time import fake_time


class MockWrapper():
    """Wraps a time faker with mocks."""

    def __init__(self, faker: fake_time.FakeTime):
        super().__init__()
        self.sleep = mock.Mock(wraps=faker.sleep)
        self.time = mock.Mock(wraps=faker.time)
        self.time_ns = mock.Mock(wraps=faker.time_ns)
        self.monotonic = mock.Mock(wraps=faker.monotonic)
        self.monotonic_ns = mock.Mock(wraps=faker.monotonic_ns)

    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Install this fake timer into time using monkeypatch."""
        monkeypatch.setattr("time.sleep", self.sleep)
        monkeypatch.setattr("time.time_ns", self.time_ns)
        monkeypatch.setattr("time.time", self.time)
        monkeypatch.setattr("time.monotonic_ns", self.monotonic_ns)
        monkeypatch.setattr("time.monotonic", self.monotonic)
