######################
 Recording Time Calls
######################

Pytest-time also provides ``mock_time``, a fixture that wraps several ``time`` functions
in Mock objects but still runs the real calls. This is useful if you need to ensure that
certain calls occurred, etc. The fixture will provide Mock objects for inspection in
tests:

.. code-block:: python

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

*********************************
 Mocking time with instant sleep
*********************************

The ``mock_instant_sleep`` fixture combines :doc:`instant_sleep` with ``mock_time``.
This fixture replaces the relevant ``time`` functions as in the ``instant_sleep``
fixture, but also provides mock wrappers around those functions, allowing for recording
time.

.. code-block:: python

    import time


    def test_mock_instant_sleep(mock_instant_sleep):
        start_time = time.time()
        start_monotonic = time.monotonic()

        time.sleep(86400)  # Doesn't sleep

        assert time.time() >= start_time + 86400
        assert time.monotonic() >= start_monotonic + 86400

        mock_instant_sleep.sleep.assert_called_once_with(86400)
        assert len(mock_instant_sleep.time.mock_calls) == 2
        assert len(mock_instant_sleep.monotonic.mock_calls) == 2
