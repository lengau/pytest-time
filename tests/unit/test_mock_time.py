"""Tests for the MockWrapper."""
import time
from unittest import mock

import pytest
import pytest_check

from pytest_time import fake_time, real_time, wrap_time


@pytest.fixture
def mock_wrapper():
    mock_faker = mock.Mock(spec=fake_time.FakeTime)
    return wrap_time.MockWrapper(mock_faker)


def test_install(monkeypatch, mock_wrapper):
    def check_monkeypatch(fn: str, cls):
        patched = getattr(time, fn)
        original = getattr(real_time, fn)
        new = getattr(cls, fn)
        pytest_check.not_equal(original, new)
        pytest_check.equal(patched, new)
        pytest_check.not_equal(patched, original)

    mock_wrapper.install(monkeypatch)

    check_monkeypatch("sleep", mock_wrapper)
    check_monkeypatch("time_ns", mock_wrapper)
    check_monkeypatch("time", mock_wrapper)
    check_monkeypatch("monotonic_ns", mock_wrapper)
    check_monkeypatch("monotonic", mock_wrapper)
