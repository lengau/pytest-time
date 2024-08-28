"""Tests for the instant sleep time faker."""
import time

import pytest
import pytest_check
from hypothesis import given, strategies

from pytest_time import InstantSleep, real_time


@pytest.fixture
def faker(monkeypatch):
    fake = InstantSleep()
    fake.install(monkeypatch)
    return fake


@given(sleep_time=strategies.floats(min_value=10**-3, max_value=2**32))
def test_instant_sleep_doesnt_sleep_time(sleep_time):
    """Test that we sleep for far less time than given.

    We're keeping the min value to 1 ms so CI should run it.
    """
    faker = InstantSleep()
    with pytest.MonkeyPatch.context() as mp:
        faker.install(mp)

        fake_before = time.time()
        real_before = real_time.time()
        time.sleep(sleep_time)
        fake_after = time.time()
        real_after = real_time.time()

    fake_delta = fake_after - fake_before
    real_delta = real_after - real_before

    pytest_check.greater_equal(
        fake_delta, sleep_time, "Fake time module didn't sleep for long enough"
    )
    pytest_check.less(real_delta, sleep_time, "Took too much real time.")


@given(sleep_time=strategies.floats(min_value=10**-3, max_value=2**32))
def test_instant_sleep_doesnt_sleep_monotonic(sleep_time):
    """Test that we sleep for far less time than given.

    We're keeping the min value to 1 ms so CI should run it.
    """
    faker = InstantSleep()
    with pytest.MonkeyPatch.context() as mp:
        faker.install(mp)

        fake_before = time.monotonic()
        real_before = real_time.monotonic()
        time.sleep(sleep_time)
        fake_after = time.monotonic()
        real_after = real_time.monotonic()

    fake_delta = fake_after - fake_before
    real_delta = real_after - real_before

    pytest_check.greater_equal(
        fake_delta, sleep_time, "Fake time module didn't sleep for long enough"
    )
    pytest_check.less(real_delta, sleep_time, "Took too much real time.")
