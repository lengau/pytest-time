Instant sleep
=============

The ``instant_sleep`` fixture is the most basic wrapper and is designed to be used at
any scope. It monkeypatches the built-in ``time`` module to be chronologically
consistent while not actually sleeping when running ``time.sleep``. This includes
modifying the behaviour of ``time.time()``, ``time.monotonic()`` and their nanosecond
counterparts to include the additional delay expected after sleeping.

A basic use of ``instant_sleep`` is shown below:

.. code-block:: python

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

This code will behave almost identically with and without the ``instant_sleep`` fixture
in use. To demonstrate, let's time this file with the fixture enabled...

.. code-block:: text

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

.. code-block:: text

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

The sleep is, for practical purposes, essentially instant. And yet, the ``time`` module
still acts as though the appropriate time has passed.

.. autofunction:: pytest_time.instant_sleep
