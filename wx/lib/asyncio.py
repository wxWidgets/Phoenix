#----------------------------------------------------------------------
# Name:        wx.lib.asyncio
# Purpose:     Coroutine support for event handlers
#
# Author:      XU Guang-zhao 徐广钊
#
# Created:     8-Dec-2018
# Copyright:   (C) 2018 XU Guang-zhao 徐广钊
# Licence:     wxWidgets license
#
# Tags:        documented
#
#----------------------------------------------------------------------

"""
Add ``wx.BindAsync()`` and other supporting classes to enable coroutine_
support for wxPython.

.. _coroutine: https://docs.python.org/3/library/asyncio-task.html#coroutine

Description
===========
Before the introduction of coroutines, developers for GUI applications have to ways
to handle time-consuming tasks. One of them is ``wx.Yield()`` which periodically
yield the control to wxPython and let events to be processed. This is straitforward
but performance issues are usually encountered, and users may frequently observe lags
or busy cursors. Another one of them is to launch the task in another thread, however
due to the complexity of GUI frameworks, UI elements can only be updated in the main
thread, leading to the wide usage of ``wx.CallAfter()`` and callbacks. As the program
logic increases, developers will eventually realize that they have already felt into
the so-called "Callback Hell", and they will spend most of their time in taking care of
the program states among these callbacks, because the program logic is usually in series
but the program must be implemented in an asynchronous way. Considering such a situation:
When a button is clicked a file will be downloaded, and then a CPU-intensive thread will
be launched to process the data. With bare ``wx.CallAfter()`` there will be at least two
callbacks, and what will happen if we need more, for example retrying the download when
it fails?

Coroutines are introduced to solve this problem. Time-consuming or IO-bound tasks can be
wrapped into "awaitables" and ``await``-ed in coroutines; a coroutine will be
automatically suspended when it is trapped in an "awaitable", and woke up when the task
finishes. Additionally, as all coroutines (all coroutines launched in the main event
loop, exactly) will be executed in the main thread, there will be no worry about any
confilction caused by concurrency in the program logic.

Usage
=====
Sample usage::
    #!/usr/bin/env python3
    import asyncio
    import threading
    import time

    import wx
    import wx.lib.asyncio

    def main():
        asyncio.get_event_loop().set_debug(True)

        def _another_loop_thread():
            nonlocal another_loop
            another_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(another_loop)
            another_loop.run_forever()
            another_loop.close()

        another_loop = None
        another_loop_thread = threading.Thread(target=_another_loop_thread)
        another_loop_thread.start()

        def on_close(event):
            another_loop.call_soon_threadsafe(another_loop.stop)
            frame.Destroy()

        frame = wx.Frame(None, title='Coroutine Integration in wxPython', size=wx.Size(800, 600))
        frame.Bind(wx.EVT_CLOSE, on_close)
        frame.CreateStatusBar()
        frame.GetStatusBar().StatusText = 'Ready'
        counter = 1

        async def on_click(event):
            def log(message: str):
                frame.GetStatusBar().StatusText = message
                print(message)

            nonlocal counter
            count = ' [' + str(counter) + ']'
            counter += 1
            log('Starting the event handler' + count)
            await asyncio.sleep(1)  # Sleep in the current event loop
            log('Running in the thread pool' + count)
            # time.sleep is used to emulate synchronous time-consuming tasks
            await asyncio.get_event_loop().run_in_executor(None, time.sleep, 1)
            log('Running in another loop' + count)
            # Socket operations are theoretically unsupported in WxEventLoop
            # So a default event loop in a separate thread is sometime required
            # asyncio.sleep is used to emulate these asynchronous tasks
            await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(asyncio.sleep(1), another_loop))
            log('Ready' + count)

        button = wx.Button(frame, label='\n'.join([
            'Click to start the asynchronous event handler',
            'The application will remain responsive while the handler is running',
            'Try click here multiple times to launch multiple coroutines',
            'These coroutines will not conflict each other as they are all in the same thread',
        ]))
        button.BindAsync(wx.EVT_BUTTON, on_click)

        frame.Show()

        asyncio.get_event_loop().run_forever()
        another_loop_thread.join()


    if __name__ == '__main__':
        asyncio.set_event_loop_policy(wx.lib.asyncio.WxEventLoopPolicy(app=wx.App))
        main()

"""

#!/usr/bin/env python3
import asyncio
import concurrent.futures
import threading
import time
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from typing import Optional, Callable, Any, Type

import wx


class WxTimerHandle(asyncio.TimerHandle):
    __slots__ = 'call_later',


class WxEventLoop(asyncio.AbstractEventLoop):
    def __init__(self, app: wx.AppConsole):
        self._closed = False
        self._app = app
        self._default_executor = None
        self._debug = False
        self._exception_handler = None
        self._task_factory = None

    def run_forever(self) -> None:
        self._app.MainLoop()

    def stop(self) -> None:
        self._app.ExitMainLoop()

    def is_running(self) -> bool:
        return self._app.GetMainLoop() is not None

    def close(self) -> None:
        executor = self._default_executor
        if executor is not None:
            self._default_executor = None
            executor.shutdown(wait=False)
        self._closed = True

    def _timer_handle_cancelled(self, handle: WxTimerHandle) -> None:
        handle.call_later.Stop()

    def call_soon(self, callback: Callable[..., Any], *args, context=None) -> None:
        self.call_soon_threadsafe(callback, *args)

    def call_at(self, when, callback: Callable[..., Any], *args, context=None) -> WxTimerHandle:
        return self.call_later(when - self.time(), callback, *args, context)

    def call_later(self, delay: float, callback: Callable[..., Any], *args: Any) -> WxTimerHandle:
        handle = WxTimerHandle(delay * 1000 + self.time(), callback, args, self)
        handle.call_later = wx.CallLater(int(delay * 1000), callback, *args)
        return handle

    def time(self) -> float:
        return time.monotonic()

    def create_future(self) -> asyncio.Future:
        return asyncio.Future(loop=self)

    def create_task(self, coro) -> asyncio.Task:
        if self._task_factory is None:
            return asyncio.Task(coro, loop=self)
        else:
            return self._task_factory(self, coro)

    def call_soon_threadsafe(self, callback: Callable[..., Any], *args, context=None) -> None:
        wx.CallAfter(callback, *args)

    def run_in_executor(self, executor: concurrent.futures.ThreadPoolExecutor, func: Callable[..., Any], *args) -> asyncio.Future:
        if executor is None:
            executor = self._default_executor
        if executor is None:
            executor = concurrent.futures.ThreadPoolExecutor()
            self._default_executor = executor
        return asyncio.wrap_future(executor.submit(func, *args), loop=self)

    def set_default_executor(self, executor: concurrent.futures.ThreadPoolExecutor) -> None:
        self._default_executor = executor

    def get_exception_handler(self):
        return self._exception_handler

    def set_exception_handler(self, handler):
        self._exception_handler = handler

    def default_exception_handler(self, context):
        print('Got exception: ' + repr(context))

    def call_exception_handler(self, context):
        if self._exception_handler is None:
            self.default_exception_handler(context)
        else:
            self._exception_handler(self, context)

    def get_debug(self) -> bool:
        return self._debug

    def set_debug(self, enabled: bool) -> None:
        self._debug = enabled

    def run_until_complete(self, future):
        raise NotImplementedError

    def is_closed(self) -> bool:
        return self._closed

    async def shutdown_asyncgens(self):
        raise NotImplementedError

    def set_task_factory(self, factory) -> None:
        self._task_factory = factory

    def get_task_factory(self):
        return self._task_factory


class WxEventLoopPolicy(asyncio.AbstractEventLoopPolicy):
    def __init__(self, app: Type[wx.AppConsole], delegate: asyncio.AbstractEventLoopPolicy = asyncio.get_event_loop_policy()):
        self._app = app
        self._loop = None
        self._delegate = delegate

    def get_event_loop(self) -> AbstractEventLoop:
        if threading.current_thread() is threading.main_thread():
            if self._loop is None:
                self._loop = WxEventLoop(self._app())
            return self._loop
        else:
            return self._delegate.get_event_loop()

    def set_event_loop(self, loop: AbstractEventLoop) -> None:
        self._delegate.set_event_loop(loop)

    def new_event_loop(self) -> AbstractEventLoop:
        return self._delegate.new_event_loop()

    def get_child_watcher(self) -> Any:
        return self._delegate.get_child_watcher()

    def set_child_watcher(self, watcher: Any) -> None:
        self._delegate.set_child_watcher(watcher)


def _bind_async(self, event, handler):
    def _handler(event):
        asyncio.ensure_future(handler(event))

    self.Bind(event, _handler)


wx.EvtHandler.BindAsync = _bind_async


def _test():
    asyncio.set_event_loop_policy(WxEventLoopPolicy(app=wx.App))
    asyncio.get_event_loop().set_debug(True)

    def _another_loop_thread():
        nonlocal another_loop
        another_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(another_loop)
        another_loop.run_forever()
        another_loop.close()

    another_loop = None
    another_loop_thread = threading.Thread(target=_another_loop_thread)
    another_loop_thread.start()

    def on_close(event):
        another_loop.call_soon_threadsafe(another_loop.stop)
        frame.Destroy()

    frame = wx.Frame(None, title='Coroutine Integration in wxPython', size=wx.Size(800, 600))
    frame.Bind(wx.EVT_CLOSE, on_close)
    frame.CreateStatusBar()
    frame.GetStatusBar().StatusText = 'Ready'
    counter = 1

    async def on_click(event):
        def log(message: str):
            frame.GetStatusBar().StatusText = message
            print(message)

        nonlocal counter
        count = ' [' + str(counter) + ']'
        counter += 1
        log('Starting the event handler' + count)
        await asyncio.sleep(1)  # Sleep in the current event loop
        log('Running in the thread pool' + count)
        # time.sleep is used to emulate synchronous time-consuming tasks
        await asyncio.get_event_loop().run_in_executor(None, time.sleep, 1)
        log('Running in another loop' + count)
        # Socket operations are theoretically unsupported in WxEventLoop
        # So a default event loop in a separate thread is sometime required
        # asyncio.sleep is used to emulate these asynchronous tasks
        await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(asyncio.sleep(1), another_loop))
        log('Ready' + count)

    button = wx.Button(frame, label='\n'.join([
        'Click to start the asynchronous event handler',
        'The application will remain responsive while the handler is running',
        'Try click here multiple times to launch multiple coroutines',
        'These coroutines will not conflict each other as they are all in the same thread',
    ]))
    button.BindAsync(wx.EVT_BUTTON, on_click)

    frame.Show()

    asyncio.get_event_loop().run_forever()
    another_loop_thread.join()


if __name__ == '__main__':
    _test()
