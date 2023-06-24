"""Pytester test for testing mock_instant_sleep."""

import time


def test_mock_instant_sleep(mock_instant_sleep):
    start_time = time.time()
    start_monotonic = time.monotonic()

    time.sleep(86400)

    assert time.time() >= start_time + 86400
    assert time.monotonic() >= start_monotonic + 86400

    mock_instant_sleep.sleep.assert_called_once_with(86400)
    assert len(mock_instant_sleep.time.mock_calls) == 2
    assert len(mock_instant_sleep.monotonic.mock_calls) == 2
