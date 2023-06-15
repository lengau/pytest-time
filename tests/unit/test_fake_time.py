"""Tests for the fake_time module."""
import time

import pytest
import pytest_check

from pytest_time import fake_time, real_time

NS_TO_SEC = [
    (0, 0),
    (1, 0.000_000_001),
    (1_000_000, 0.001),
    (1_000_000_000, 1),
]


@pytest.mark.parametrize(("ns", "sec"), NS_TO_SEC)
def test_ns_to_sec(ns, sec):
    assert fake_time._ns_to_sec(ns) == sec


def check_monkeypatch(fn: str, fft: fake_time.FakeTime):
    patched = getattr(time, fn)
    original = getattr(real_time, fn)
    new = getattr(fft, fn)
    pytest_check.not_equal(original, new)
    pytest_check.equal(patched, new)
    pytest_check.not_equal(patched, original)


class FakeFakeTime(fake_time.FakeTime):
    """A fake class for testing FakeTime"""

    def __init__(self, now: int = 0):
        super().__init__()
        self.now = now

    def time_ns(self) -> int:
        return self.now

    def monotonic_ns(self) -> int:
        return self.now


def test_fake_time_install(monkeypatch):
    fft = FakeFakeTime()

    fft.install(monkeypatch)

    check_monkeypatch("sleep", fft)
    check_monkeypatch("time_ns", fft)
    check_monkeypatch("time", fft)
    check_monkeypatch("monotonic_ns", fft)
    check_monkeypatch("monotonic", fft)


@pytest.mark.parametrize(("ns", "sec"), NS_TO_SEC)
def test_fake_time_time(ns, sec):
    fft = FakeFakeTime(ns)

    assert fft.time() == sec


@pytest.mark.parametrize(("ns", "sec"), NS_TO_SEC)
def test_fake_time_monotonic(ns, sec):
    fft = FakeFakeTime(ns)

    assert fft.monotonic() == sec
