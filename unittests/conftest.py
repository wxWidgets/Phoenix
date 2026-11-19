import sys
import traceback
import warnings

import pytest


class CallbackExceptionWarning(UserWarning):
    """
    A test left an exception in sys.last_exc, where Python stores exceptions
    that wxPython prints from event handlers and other callbacks. Its
    traceback keeps the callback's locals alive until the next test, and on
    macOS deleting some of them (such as DCs) that late can crash.
    """


def _lastException():
    # sys.last_exc is new in Python 3.12
    return getattr(sys, 'last_exc', None) or getattr(sys, 'last_value', None)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    report = yield
    if report.when == 'call':
        item.callFailed = report.failed
    return report


@pytest.fixture(autouse=True)
def checkCallbackExceptions(request):
    before = _lastException()
    yield
    exc = _lastException()
    # pytest stores the exception of a failing test there too
    if exc is None or exc is before or getattr(request.node, 'callFailed', False):
        return
    where = ''
    if exc.__traceback__ is not None:
        frame = traceback.extract_tb(exc.__traceback__)[-1]
        where = f' (raised at {frame.filename}:{frame.lineno} in {frame.name})'
    warnings.warn(f'exception in a callback: {type(exc).__name__}: {exc}{where}',
                  CallbackExceptionWarning)
