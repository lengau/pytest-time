"""PyTester test for just wrapping the time module."""

import time


def test_mock_time(mock_time):
    start_time = time.time()
    start_monotonic = time.monotonic()

    time.sleep(1)  # Actually sleeps for a second

    assert time.time() >= start_time + 1
    assert time.monotonic() >= start_monotonic + 1

    mock_time.sleep.assert_called_once_with(1)
    assert len(mock_time.time.mock_calls) == 2
    assert len(mock_time.monotonic.mock_calls) == 2
