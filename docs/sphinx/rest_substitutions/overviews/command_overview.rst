.. include:: headings.inc


.. _command overview:

=====================================
|phoenix_title|  **Command Overview**
=====================================


:class:`wx.Command` is a base class for modelling an application
command, which is an action usually performed by selecting a menu
item, pressing a toolbar button or any other means provided by the
application to change the data or view.

Instead of the application functionality being scattered around if
statements and functions in a way that may be hard to read and
maintain, the functionality for a command is explicitly represented as
an object which can be manipulated by a framework or application.

When a user interface event occurs, the application submits a command
to a :class:`wx.CommandProcessor` object to execute and store.

The wxPython document/view framework handles Undo and Redo by use of
:class:`wx.Command` and :class:`wx.CommandProcessor` objects. You
might find further uses for :class:`Command`, such as implementing a
macro facility that stores, loads and replays commands.

An application can derive a new class for every command, or, more
likely, use one class parameterized with an integer or string command
identifier.


.. _commandprocessor overview:

=================================================
|phoenix_title|  **CommandProcessor Overview**
=================================================


:class:`wx.CommandProcessor` is a class that maintains a history of
:class:`wx.Command` instances, with undo/redo functionality
built-in. Derive a new class from this if you want different
behaviour.


.. _filehistory overview:

=================================================
|phoenix_title|  **FileHistory Overview**
=================================================

:class:`wx.FileHistory` encapsulates functionality to record the last
few files visited, and to allow the user to quickly load these files
using the list appended to the File menu. Although
:class:`wx.FileHistory` is used by :class:`wx.DocManager`, it can be
used independently. You may wish to derive from it to allow different
behaviour, such as popping up a scrolling list of files.

By calling :meth:`wx.FileHistory.UseMenu` you can associate a file
menu with the file history. The menu will then be used for appending
filenames that are added to the history.

.. note::

   Please notice that currently if the history already contained
   filenames when UseMenu() is called (e.g. when initializing a second
   MDI child frame), the menu is not automatically initialized with
   the existing filenames in the history and so you need to call
   :meth:`wx.FileHistory.AddFilesToMenu` after UseMenu() explicitly in
   order to initialize the menu with the existing list of MRU files
   (otherwise an assertion failure is raised in debug builds).

The filenames are appended using menu identifiers in the range
``wx.ID_FILE1`` to ``wx.ID_FILE9``.



