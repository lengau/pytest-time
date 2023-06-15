"""Pytest plugin for manipulating the time."""

from pytest_time.fake_time import FakeTime
from pytest_time import real_time
from pytest_time.instant_sleep import InstantSleep

__all__ = ["FakeTime", "InstantSleep", "real_time"]
