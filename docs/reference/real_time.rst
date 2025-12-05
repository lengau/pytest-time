####################################
 Access to the real ``time`` module
####################################

The ``pytest_time.real_time`` module in contains references to the real implementations
of everything in the built-in :external+python:doc:`time <library/time>` module. If your
tests need to reference the real ``time`` module, they can do so with ``from pytest_time
import real_time``.
