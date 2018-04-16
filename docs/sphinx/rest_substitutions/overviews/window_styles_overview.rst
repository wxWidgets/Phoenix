.. include:: headings.inc


.. _window styles:

=================================================
|phoenix_title|  **Window Styles Overview**
=================================================


Window styles are used to specify alternative behaviour and
appearances for windows, when they are created.

The symbols are defined in such a way that they can be combined in a
'bit-list' using the Python `bitwise-or` operator (``|``).

For example::

    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER


For the window styles specific to each window class, please see the
documentation for the window.

Most windows can use the generic styles listed for :ref:`wx.Window` in
addition to their own styles.
