"""Integration tests for InstantSleep."""


def test_instant_sleep(pytester):
    pytester.copy_example("test_instant_sleep.py")
    result = pytester.runpytest("-k", "test_instant_sleep")

    result.assert_outcomes(passed=15)


def test_mock_time(pytester):
    pytester.copy_example("test_mock_time.py")
    result = pytester.runpytest("-k", "test_mock_time")

    result.assert_outcomes(passed=1)


def test_mock_instant_sleep(pytester):
    pytester.copy_example("test_mock_instant_sleep.py")
    result = pytester.runpytest("-k", "test_mock_instant_sleep")

    result.assert_outcomes(passed=1)
