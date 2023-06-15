"""Fixtures etc. for pytest-time plugin."""

import pytest

from pytest_time import InstantSleep


@pytest.fixture()
def instant_sleep(monkeypatch: pytest.MonkeyPatch) -> InstantSleep:
    """Fixture for speeding through time.sleep."""
    sleep = InstantSleep()
    sleep.install(monkeypatch)
    return sleep
