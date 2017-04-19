.. include:: headings.inc


.. _window deletion:

=============================================
|phoenix_title|  **Window Deletion Overview**
=============================================


Window deletion can be a confusing subject, so this overview is
provided to help make it clear when and how you delete windows, or
respond to user requests to close windows.



Sequence of Events During Window Deletion
-----------------------------------------

When the user clicks on the system close button or system close
command, in a frame or a dialog, wxPython calls
:meth:`wx.Window.Close`.  This in turn generates an ``wx.EVT_CLOSE``
event: see :ref:`wx.CloseEvent`.

It is the duty of the application to define a suitable event handler,
and decide whether or not to destroy the window. If the application is
for some reason forcing the application to close
(:meth:`wx.CloseEvent.CanVeto` returns ``False``), the window should
always be destroyed, otherwise there is the option to ignore the
request, or maybe wait until the user has answered a question before
deciding whether it is safe to close. The handler for ``wx.EVT_CLOSE``
should signal to the calling code if it does not destroy the window,
by calling :meth:`wx.CloseEvent.Veto`. Calling this provides useful
information to the calling code.

The :ref:`wx.CloseEvent` handler should only call
:meth:`wx.Window.Destroy` to delete the window, and not use the `del`
operator. This is because for some window classes, wxPython delays
actual deletion of the window until all events have been processed,
since otherwise there is the danger that events will be sent to a
non-existent window.

As reinforced in the next section, calling `Close` does not guarantee
that the window will be destroyed. Call :meth:`wx.Window.Destroy` if
you want to be certain that the window is destroyed.



Closing Windows
---------------

Your application can either use :meth:`wx.Window.Close` event just as
the framework does, or it can call :meth:`wx.Window.Destroy` directly.
If using `Close()`, you can pass a ``True`` argument to this function
to tell the event handler that we definitely want to delete the frame
and it cannot be vetoed.

The advantage of using `Close` instead of `Destroy` is that it will
call any clean-up code defined by the ``wx.EVT_CLOSE`` handler; for
example it may close a document contained in a window after first
asking the user whether the work should be saved. `Close` can be
vetoed by this process (return ``False``), whereas `Destroy`
definitely destroys the window.



Default Window Close Behaviour
------------------------------

The default close event handler for :ref:`wx.Dialog` simulates a
``Cancel`` command, generating a ``wx.ID_CANCEL`` event. Since the
handler for this cancel event might itself call `Close`, there is a
check for infinite looping. The default handler for ``wx.ID_CANCEL``
hides the dialog (if modeless) or calls `EndModal(wx.ID_CANCEL)` (if
modal). In other words, by default, the dialog is not destroyed.

The default close event handler for :ref:`wx.Frame` destroys the frame
using `Destroy()`.



User Calls to Exit From a Menu
------------------------------

What should I do when the user calls up `Exit` from a menu? You can
simply call :meth:`wx.Window.Close` on the frame. This will invoke
your own close event handler which may destroy the frame.

You can do checking to see if your application can be safely exited at
this point, either from within your close event handler, or from
within your exit menu command handler. For example, you may wish to
check that all files have been saved. Give the user a chance to save
and quit, to not save but quit anyway, or to cancel the exit command
altogether.



Exiting the Application Gracefully
----------------------------------

A wxPython application automatically exits when the last top level
window (:ref:`wx.Frame` or :ref:`wx.Dialog`), is destroyed. Put any
application-wide cleanup code in :meth:`wx.AppConsole.OnExit` (this is
a method, not an event handler).



Automatic Deletion of Child Windows
-----------------------------------

Child windows are deleted from within the parent destructor. This
includes any children that are themselves frames or dialogs, so you
may wish to close these child frame or dialog windows explicitly from
within the parent close handler.



Other Kinds of Windows
----------------------

So far we've been talking about 'managed' windows, i.e. frames and
dialogs. Windows with parents, such as controls, don't have delayed
destruction and don't usually have close event handlers, though you
can implement them if you wish. For consistency, continue to use the
:meth:`wx.Window.Destroy` method instead of the `del` operator when
deleting these kinds of windows explicitly.

