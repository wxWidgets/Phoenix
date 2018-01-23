.. include:: headings.inc


.. _drag and drop overview:

===========================================
|phoenix_title|  **Drag and Drop Overview**
===========================================


It may be noted that data transfer to and from the clipboard is quite
similar to data transfer with drag and drop and the code to implement
these two types is almost the same. In particular, both data transfer
mechanisms store data in some kind of :ref:`wx.DataObject` and identify
its format(s) using the :ref:`wx.DataFormat` class.

To be a `drag` source, i.e. to provide the data which may be dragged
by the user elsewhere, you should implement the following steps:

- **Preparation**: First of all, a data object must be created and
  initialized with the data you wish to drag. For example::

      my_data = wx.TextDataObject("This text will be dragged.")



- **Drag start**: To start the dragging process (typically in response
  to a mouse click) you must call :meth:`wx.DropSource.DoDragDrop` like
  this::

      dragSource = wx.DropSource(self)
      dragSource.SetData(my_data)
      result = dragSource.DoDragDrop(True)



- **Dragging**: The call to `DoDragDrop()` blocks the program until
  the user releases the mouse button (unless you override the
  :meth:`wx.DropSource.GiveFeedback` function to do something
  special). When the mouse moves in a window of a program which
  understands the same drag-and-drop protocol (any program under
  Windows or any program supporting the XDnD protocol under X
  Windows), the corresponding :ref:`wx.DropTarget` methods are called -
  see below.

- **Processing the result**: `DoDragDrop()` returns an effect code
  which is one of the values of :ref:`wx.DragResult`::

      if result == wx.DragCopy:
          # Copy the data
          CopyMyData()

      elif result == wx.DragMove:
          # Move the data
          MoveMyData()

      else:
          # Default, do nothing
          pass


To be a `drop` target, i.e. to receive the data dropped by the user
you should follow the instructions below:

- **Initialization**: For a window to be a drop target, it needs to
  have an associated :ref:`wx.DropTarget` object. Normally, you will
  call :meth:`wx.Window.SetDropTarget` during window creation
  associating your drop target with it. You must derive a class from
  :ref:`wx.DropTarget` and override its pure virtual
  methods. Alternatively, you may derive from :ref:`wx.TextDropTarget`
  or :ref:`wx.FileDropTarget` and override their `OnDropText()` or
  `OnDropFiles()` method.

- **Drop**: When the user releases the mouse over a window, wxPython
  asks the associated :ref:`wx.DropTarget` object if it accepts the
  data. For this, a :ref:`wx.DataObject` must be associated with the
  drop target and this data object will be responsible for the format
  negotiation between the drag source and the drop target. If all goes
  well, then :meth:`wx.DropTarget.OnData` will get called and the
  :ref:`wx.DataObject` belonging to the drop target can get filled
  with data.

- **The end**: After processing the data, `DoDragDrop()` returns
  either ``wx.DragCopy`` or ``wx.DragMove`` depending on the state of
  the keys ``Ctrl``, ``Shift`` and ``Alt`` at the moment of the
  drop. There is currently no way for the drop target to change this
  return code.


