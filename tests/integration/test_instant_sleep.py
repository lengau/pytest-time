"""Integration tests for InstantSleep"""


def test_instant_sleep(pytester):
    pytester.copy_example("test_instant_sleep.py")
    result = pytester.runpytest("-k", "test_instant_sleep")

    result.assert_outcomes(passed=12)
