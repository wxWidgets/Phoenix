.. include:: headings.inc


.. _log classes overview:
.. _logging overview:

===============================================
|phoenix_title|  **Log Classes Overview**
===============================================


Introduction
------------

This is a general overview of logging classes provided by
wxPython. The word logging here has a broad sense, including all of
the program output, not only non-interactive messages. The logging
facilities included in wxPython provide the base :ref:`wx.Log` class
which defines the standard interface for a log target as well as
several standard implementations of it and a family of functions to
use with them.

First of all, no knowledge of :ref:`wx.Log` classes is needed to use
them. For this, you should only know about :func:`wx.LogDebug`,
:func:`wx.LogError`, :func:`wx.LogMessage` and similar functions. All of
them have the same syntax as the Python `logging
<http://docs.python.org/library/logging.html>`_ module.

Here are all of them:

- :func:`wx.LogFatalError` which is like :func:`wx.LogError`, but also
  terminates the program with the exit code 3 (using `abort()`
  standard function). Unlike for all the other logging functions, this
  function can't be overridden by a log target.

- :func:`wx.LogError` is the function to use for error messages, i.e. the
  messages that must be shown to the user.  The default processing is
  to pop up a message box to inform the user about it.

- :func:`wx.LogWarning` for warnings. They are also normally shown to the
  user, but don't interrupt the program work.

- :func:`wx.LogMessage` is for all normal, informational messages. They
  also appear in a message box by default (but it can be changed, see
  below).

- :func:`wx.LogVerbose` is for verbose output. Normally, it is
  suppressed, but might be activated if the user wishes to know more
  details about the program progress (another, but possibly confusing
  name for the same function is :func:`wx.LogInfo`).

- :func:`wx.LogStatus` is for status messages. They will go into the
  status bar of the active or specified (as the first argument)
  :ref:`wx.Frame` if it has one.

- :func:`wx.LogSysError` is mostly used by wxPython itself, but might be
  handy for logging errors after system call (API function)
  failure. It logs the specified message text as well as the last
  system error code (`errno` or Windows' `GetLastError()` depending on
  the platform) and the corresponding error message. The second form
  of this function takes the error code explicitly as the first
  argument.

- :func:`wx.LogDebug` is the right function for debug output. It only
  does anything at all in the debug mode (when the preprocessor symbol
  ``__WXDEBUG__`` is defined) and expands to nothing in release mode
  (otherwise). Note that under Windows, you must either run the
  program under debugger or use a 3rd party program such as
  **DebugView**
  (http://www.microsoft.com/technet/sysinternals/Miscellaneous/DebugView.mspx)
  to actually see the debug output.

- :func:`wx.LogTrace` as :func:`wx.LogDebug` only does something in debug
  build. The reason for making it a separate function from it is that
  usually there are a lot of trace messages, so it might make sense to
  separate them from other debug messages which would be flooded in
  them. Moreover, the second version of this function takes a trace
  mask as the first argument which allows to further restrict the
  amount of messages generated.


The usage of these functions should be fairly straightforward, however
it may be asked why not use the other logging facilities, such as the
Python `logging <http://docs.python.org/library/logging.html>`_
module. The short answer is that they're all very good generic
mechanisms, but are not really adapted for wxPython, while the log
classes are. However every project is different with different needs,
so you are encouraged to investigate all options and use what works
best for you

Some of advantages in using wxPython log functions are:

- Portability

- Flexibility: The output of :ref:`wx.Log` functions can be redirected or
  suppressed entirely based on their importance, which is either
  impossible or difficult to do with traditional methods. For example,
  only error messages, or only error messages and warnings might be
  logged, filtering out all informational messages.

- Completeness: Usually, an error message should be presented to the
  user when some operation fails. Let's take a quite simple but common
  case of a file error: suppose that you're writing your data file on
  disk and there is not enough space. The actual error might have been
  detected inside wxPython code, so the calling function doesn't
  really know the exact reason of the failure, it only knows that the
  data file couldn't be written to the disk. However, as wxPython uses
  :func:`wx.LogError` in this situation, the exact error code (and the
  corresponding error message) will be given to the user together with
  "high level" message about data file writing error.



.. _log messages selection:

Log Messages Selection
----------------------

By default, most log messages are enabled. In particular, this means
that errors logged by wxPython code itself (e.g. when it fails to
perform some operation) will be processed and shown to the user. To
disable the logging entirely you can use :meth:`wx.Log.EnableLogging`
method or, more usually, :ref:`wx.LogNull` class which temporarily
disables logging and restores it back to the original setting when it
is destroyed.

To limit logging to important messages only, you may use
:meth:`wx.Log.SetLogLevel` with e.g. ``wx.LOG_Warning`` value -- this
will completely disable all logging messages with the severity less
than warnings, so :func:`wx.LogMessage` output won't be shown to the
user any more.

Moreover, the log level can be set separately for different log
components. Before showing how this can be useful, let us explain what
log components are: they are simply arbitrary strings identifying the
component, or module, which generated the message. They are
hierarchical in the sense that "foo/bar/baz" component is supposed to
be a child of "foo". And all components are children of the unnamed
root component.

By default, all messages logged by wxPython originate from "wx"
component or one of its subcomponents such as "wx/net/ftp", while the
messages logged by your own code are assigned empty log component. To
change this, you need to define ``wx.LOG_COMPONENT`` to a string uniquely
identifying each component, e.g. you could give it the value
"MyProgram" by default and re-define it as "MyProgram/DB" in the
module working with the database and "MyProgram/DB/Trans" in its part
managing the transactions. Then you could use
:meth:`wx.Log.SetComponentLevel` in the following ways::

        # Disable all database error messages, everybody knows databases never
        # fail anyhow
        wx.Log.SetComponentLevel("MyProgram/DB", wx.LOG_FatalError)

        # but enable tracing for the transactions as somehow our changes don't
        # get committed sometimes
        wx.Log.SetComponentLevel("MyProgram/DB/Trans", wx.LOG_Trace)

        # also enable tracing messages from wxPython dynamic module loading
        # mechanism
        wx.Log.SetComponentLevel("wx/base/module", wx.LOG_Trace)



Notice that the log level set explicitly for the transactions code
overrides the log level of the parent component but that all other
database code subcomponents inherit its setting by default and so
won't generate any log messages at all.



.. _log targets:

Log Targets
-----------

After having enumerated all the functions which are normally used to
log the messages, and why would you want to use them, we now describe
how all this works.

wxPython has the notion of a `log target`: it is just a class deriving
from :ref:`wx.Log`. As such, it implements the virtual functions of the
base class which are called when a message is logged. Only one log
target is active at any moment, this is the one used by `LogXXX`
functions. The normal usage of a log object (i.e. object of a class
derived from :ref:`wx.Log`) is to install it as the active target with a
call to `SetActiveTarget()` and it will be used automatically by all
subsequent calls to `LogXXX` functions.

To create a new log target class you only need to derive it from
:ref:`wx.Log` and override one or several of :meth:`wx.Log.DoLogRecord`,
:meth:`wx.Log.DoLogTextAtLevel` and :meth:`wx.Log.DoLogText` in it. The
first one is the most flexible and allows you to change the formatting
of the messages, dynamically filter and redirect them and so on -- all
log messages, except for those generated by :func:`wx.LogFatalError`,
pass by this function. :meth:`wx.Log.DoLogTextAtLevel` should be
overridden if you simply want to redirect the log messages somewhere
else, without changing their formatting. Finally, it is enough to
override :meth:`wx.Log.DoLogText` if you only want to redirect the log
messages and the destination doesn't depend on the message log level.

There are some predefined classes deriving from :ref:`wx.Log` and which
might be helpful to see how you can create a new log target class and,
of course, may also be used without any change. There are:

- :ref:`wx.LogStderr`: This class logs messages to the ``C`` stderr stream.

- :ref:`wx.LogGui`: This is the standard log target for wxPython
  applications (it is used by default if you don't do anything) and
  provides the most reasonable handling of all types of messages for
  given platform.

- :ref:`wx.LogWindow`: This log target provides a "log console" which
  collects all messages generated by the application and also passes
  them to the previous active log target. The log window frame has a
  menu allowing user to clear the log, close it completely or save all
  messages to file.

- :ref:`wx.LogBuffer`: This target collects all the logged messages in an
  internal buffer allowing to show them later to the user all at once.

- :ref:`wx.LogNull`: The last log class is quite particular: it doesn't
  do anything. The objects of this class may be instantiated to
  (temporarily) suppress output of `LogXXX` functions.


The log targets can also be combined: for example you may wish to
redirect the messages somewhere else (for example, to a log file) but
also process them as normally. For this the :ref:`wx.LogChain`,
:ref:`wx.LogInterposer`, and :ref:`wx.LogInterposerTemp` can be used.



.. _logging in multi-threaded applications:

Logging in Multi-Threaded Applications
--------------------------------------

Starting with wxPython 2.9.1, logging functions can be safely called
from any thread. Messages logged from threads other than the main one
will be buffered until :meth:`wx.Log.Flush` is called in the main thread
(which usually happens during idle time, i.e. after processing all
pending events) and will be really output only then. Notice that the
default GUI logger already only output the messages when it is
flushed, so by default messages from the other threads will be shown
more or less at the same moment as usual. However if you define a
custom log target, messages may be logged out of order, e.g. messages
from the main thread with later timestamp may appear before messages
with earlier timestamp logged from other threads. :ref:`wx.Log` does
however guarantee that messages logged by each thread will appear in
order in which they were logged.

Also notice that :meth:`wx.Log.EnableLogging` and :ref:`wx.LogNull` class
which uses it only affect the current thread, i.e. logging messages
may still be generated by the other threads after a call to
`EnableLogging(False)`.



.. _logging customization:

Logging Customization
---------------------

To completely change the logging behaviour you may define a custom log
target. For example, you could define a class inheriting from
:ref:`wx.Log` which shows all the log messages in some part of your main
application window reserved for the message output without
interrupting the user work flow with modal message boxes.

To use your custom log target you may either call
:meth:`wx.Log.SetActiveTarget` with your custom log object or create a
:ref:`wx.AppTraits` -derived class and override
:meth:`wx.AppTraits.CreateLogTarget` virtual method in it and also
override :meth:`wx.App.CreateTraits` to return an instance of your custom
traits object. Notice that in the latter case you should be prepared
for logging messages early during the program startup and also during
program shutdown so you shouldn't rely on existence of the main
application window, for example. You can however safely assume that
GUI is (already/still) available when your log target as used as
wxPython automatically switches to using :ref:`wx.LogStderr` if it isn't.

There are several methods which may be overridden in the derived class
to customize log messages handling: :meth:`wx.Log.DoLogRecord`,
:meth:`wx.Log.DoLogTextAtLevel` and :meth:`wx.Log.DoLogText`.

The last method is the simplest one: you should override it if you
simply want to redirect the log output elsewhere, without taking into
account the level of the message. If you do want to handle messages of
different levels differently, then you should override
:meth:`wx.Log.DoLogTextAtLevel`.

Additionally, you can customize the way full log messages are
constructed from the components (such as time stamp, source file
information, logging thread ID and so on). This task is performed by
:ref:`wx.LogFormatter` class so you need to derive a custom class from it
and override its `Format()` method to build the log messages in
desired way. Notice that if you just need to modify (or suppress) the
time stamp display, overriding `FormatTime()` is enough.

Finally, if even more control over the output format is needed, then
`LogRecord()` can be overridden as it allows to construct custom
messages depending on the log level or even do completely different
things depending on the message severity (for example, throw away all
messages except warnings and errors, show warnings on the screen and
forward the error messages to the user's (or programmer's) cell phone
-- maybe depending on whether the timestamp tells us if it is day or
night in the current time zone).



.. _using trace masks:

Using trace masks
-----------------

Notice that the use of log trace masks is hardly necessary any longer
in current wxPython version as the same effect can be achieved by
using different log components for different log statements of any
level. Please see :ref:`Log Messages Selection <log messages
selection>` for more information about the log components.

The functions below allow some limited customization of :ref:`wx.Log`
behaviour without writing a new log target class (which, aside from
being a matter of several minutes, allows you to do anything you
want). The verbose messages are the trace messages which are not
disabled in the release mode and are generated by
:func:`wx.LogVerbose`. They are not normally shown to the user because
they present little interest, but may be activated, for example, in
order to help the user find some program problem.

As for the (real) trace messages, their handling depends on the
currently enabled trace masks: if :meth:`wx.Log.AddTraceMask` was called
for the mask of the given message, it will be logged, otherwise
nothing happens.


For example::

    wx.LogTrace(wx.TRACE_OleCalls, "Foo.Bar() called")


will log the message if it was preceded by::

    wx.Log.AddTraceMask(wx.TRACE_OleCalls)


The standard trace masks are given in the :func:`wx.LogTrace`
documentation.

