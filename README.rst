pytest-time
===========

The pytest-time plugin extends pytest to control ``time`` — the built-in Python
module, not the concept within the universe.

Fixtures
--------

Pytest-time offers several fixtures for use in your projects, depending on your particular needs.

Instant Sleep
~~~~~~~~~~~~~

The ``instant_sleep`` fixture is the most basic wrapper and is designed to be used at any scope. It monkeypatches the built-in ``time`` module to be chronologically consistent while not actually sleeping when running ``time.sleep``. This includes modifying the behaviour of ``time.time()``, ``time.monotonic()`` and their nanosecond counterparts to include the additional delay expected after sleeping.

A basic use of ``instant_sleep`` is shown below:

.. code:: python

    import time
    import pytest

    @pytest.mark.parametrize("sleep_time", [1, 10, 100])
    @pytest.mark.usefixtures("instant_sleep")
    def test_instant_sleep(sleep_time):
        start_time = time.time()
        start_monotonic = time.monotonic()

        time.sleep(sleep_time)

        assert time.time() >= start_time + sleep_time
        assert time.monotonic() >= start_monotonic + sleep_time

This code will behave almost identically with and without the ``instant_sleep`` fixture in use. To demonstrate, let's time this file with the fixture enabled...

.. code:: text

    $ time pytest test_instant_sleep.py
    =========== test session starts ===========
    platform linux -- Python 3.11.4, pytest-7.3.1, pluggy-1.0.0
    rootdir: /home/lengau/Projects/pytest-time
    configfile: pyproject.toml
    plugins: check-2.1.5, mock-3.10.0, hypothesis-6.78.2, time-0.2.1.dev3+ga0d3b98.d20230624, cov-4.1.0
    collected 3 items

    test_instant_sleep.py ...                              [100%]

    =========== 3 passed in 0.01s ===========

    real    0m0.276s
    user    0m0.240s
    sys     0m0.025s

and disabled:

.. code:: text

    $ time pytest test_instant_sleep_no_fixture.py
    =========== test session starts ===========
    platform linux -- Python 3.11.4, pytest-7.3.1, pluggy-1.0.0
    rootdir: /home/lengau/Projects/pytest-time
    configfile: pyproject.toml
    plugins: check-2.1.5, mock-3.10.0, hypothesis-6.78.2, time-0.2.1.dev3+ga0d3b98.d20230624, cov-4.1.0
    collected 3 items

    test_instant_sleep_no_fixture.py ...                   [100%]

    =========== 3 passed in 111.01s (0:01:51) ===========

    real    1m51.354s
    user    0m0.250s
    sys     0m0.020s

The sleep is, for practical purposes, essentially instant. And yet, the ``time`` module still acts as though the appropriate time has passed.

Recording Time Calls
~~~~~~~~~~~~~~~~~~~~~

Pytest-time also provides ``mock_time``, a fixture that wraps several ``time`` functions in Mock objects but still runs the real calls. This is useful if you need to ensure that certain calls occurred, etc. The fixture will provide Mock objects for inspection in tests:

.. code:: python

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

Mocking a Powernap
~~~~~~~~~~~~~~~~~~

The two above are combined for you in the ``mock_instant_sleep`` fixture. This fixture replaces the relevant ``time`` functions as in the ``instant_sleep`` fixture, but also provides mock wrappers around those functions, allowing for recording time.

.. code:: python

    import time

    def test_mock_instant_sleep(mock_instant_sleep):
        start_time = time.time()
        start_monotonic = time.monotonic()

        time.sleep(86400)  # Doesn't sleep

        assert time.time() >= start_time + 86400
        assert time.monotonic() >= start_monotonic + 86400

        mock_instant_sleep.sleep.assert_called_once_with(1)
        assert len(mock_instant_sleep.time.mock_calls) == 2
        assert len(mock_instant_sleep.monotonic.mock_calls) == 2
