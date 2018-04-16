.. include:: headings.inc


.. _dialog overview:

====================================
|phoenix_title|  **Dialog Overview**
====================================


A dialog box is similar to a panel, in that it is a window which can
be used for placing controls, with the following exceptions:

- A surrounding frame is implicitly created.

- Extra functionality is automatically given to the dialog box, such
  as tabbing between items (currently Windows only).

- If the dialog box is `modal`, the calling program is blocked until
  the dialog box is dismissed.


.. seealso:: :ref:`wx.TopLevelWindow` and :ref:`wx.Window` for inherited
        member functions. Validation of data in controls is covered in
        :ref:`Validator Overview <validator overview>`.


.. _automatic scrolling dialogs:
.. _automatic scrolled dialogs:

Automatic scrolling dialogs
---------------------------

As an ever greater variety of mobile hardware comes to market, it
becomes more imperative for wxPython applications to adapt to these
platforms without putting too much burden on the programmer. One area
where wxPython can help is in adapting dialogs for the lower
resolution screens that inevitably accompany a smaller form
factor. :ref:`wx.Dialog` therefore supplies a global
:ref:`wx.DialogLayoutAdapter` class that implements automatic scrolling
adaptation for most sizer-based custom dialogs.

Many applications should therefore be able to adapt to small displays
with little or no work, as far as dialogs are concerned.  By default
this adaptation is off. To switch scrolling adaptation on globally in
your application, call the static function
:meth:`wx.Dialog.EnableLayoutAdaptation` passing ``True``. You can also
adjust adaptation on a per-dialog basis by calling
:meth:`wx.Dialog.SetLayoutAdaptationMode` with one of
``wx.DIALOG_ADAPTATION_MODE_DEFAULT`` (use the global setting),
``wx.DIALOG_ADAPTATION_MODE_ENABLED`` or
``wx.DIALOG_ADAPTATION_MODE_DISABLED``.

The last two modes override the global adaptation setting. With
adaptation enabled, if the display size is too small for the dialog,
wxPython (or rather the standard adapter class
:ref:`wx.StandardDialogLayoutAdapter`) will make part of the dialog
scrolling, leaving standard buttons in a non-scrolling part at the
bottom of the dialog. This is done as follows, in
:meth:`wx.DialogLayoutAdapter.DoLayoutAdaptation` called from within
:meth:`wx.Dialog.Show` or :meth:`wx.Dialog.ShowModal`:

- If :meth:`wx.Dialog.GetContentWindow` returns a window derived from
  :ref:`wx.BookCtrlBase`, the pages are made scrollable and no other
  adaptation is done.

- wxPython looks for a :ref:`wx.StdDialogButtonSizer` and uses it for the
  non-scrolling part.

- If that search failed, wxPython looks for a horizontal
  :ref:`wx.BoxSizer` with one or more standard buttons, with identifiers
  such as ``wx.ID_OK`` and ``wx.ID_CANCEL``.

- If that search failed too, wxPython finds 'loose' standard buttons
  (in any kind of sizer) and adds them to a
  :ref:`wx.StdDialogButtonSizer`.  If no standard buttons were found, the
  whole dialog content will scroll.

- All the children apart from standard buttons are reparented onto a
  new :ref:`wx.ScrolledWindow` object, using the old top-level sizer for
  the scrolled window and creating a new top-level sizer to lay out
  the scrolled window and standard button sizer.


.. _layout adaptation code:

Customising scrolling adaptation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to switching adaptation on and off globally and per
dialog, you can choose how aggressively wxPython will search for
standard buttons by setting
:meth:`wx.Dialog.SetLayoutAdaptationLevel`. By default, all the steps
described above will be performed but by setting the level to 1, for
example, you can choose to only look for :ref:`wx.StdDialogButtonSizer`.

You can use :meth:`wx.Dialog.AddMainButtonId` to add identifiers for
buttons that should also be treated as standard buttons for the
non-scrolling area.

You can derive your own class from :ref:`wx.DialogLayoutAdapter` or
:ref:`wx.StandardDialogLayoutAdapter` and call
:meth:`wx.Dialog.SetLayoutAdapter`, deleting the old object that this
function returns. Override the functions `CanDoLayoutAdaptation` and
`DoLayoutAdaptation` to test for adaptation applicability and perform
the adaptation.

You can also override :meth:`wx.Dialog.CanDoLayoutAdaptation` and
:meth:`wx.Dialog.DoLayoutAdaptation` in a class derived from
:ref:`wx.Dialog`.


Situations where automatic scrolling adaptation may fail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because adaptation rearranges your sizer and window hierarchy, it is
not fool-proof, and may fail in the following situations:

- The dialog doesn't use sizers.

- The dialog implementation makes assumptions about the window
  hierarchy, for example getting the parent of a control and casting
  to the dialog class.

- The dialog does custom painting and/or event handling not handled by
  the scrolled window. If this problem can be solved globally, you can
  derive a new adapter class from :ref:`wx.StandardDialogLayoutAdapter`
  and override its `CreateScrolledWindow` function to return an
  instance of your own class.

- The dialog has unusual layout, for example a vertical sizer
  containing a mixture of standard buttons and other controls.

- The dialog makes assumptions about the sizer hierarchy, for example
  to show or hide children of the top-level sizer. However, the
  original sizer hierarchy will still hold until `Show` or `ShowModal`
  is called.

You can help make sure that your dialogs will continue to function
after adaptation by:

- Avoiding the above situations and assumptions;

- Using :ref:`wx.StdDialogButtonSizer`;

- Only making assumptions about hierarchy immediately after the dialog
  is created;

- Using an intermediate sizer under the main sizer, a false top-level
  sizer that can be relied on to exist for the purposes of
  manipulating child sizers and windows;

- Overriding :meth:`wx.Dialog.GetContentWindow` to return a book control
  if your dialog implements pages: wxPython will then only make the
  pages scrollable.


PropertySheetDialog and Wizard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adaptation for :ref:`wx.PropertySheetDialog` is always done by simply
making the pages scrollable, since :meth:`wx.Dialog.GetContentWindow`
returns the dialog's book control and this is handled by the standard
layout adapter.

:class:`wx.adv.Wizard` uses its own `CanDoLayoutAdaptation` and
`DoLayoutAdaptation` functions rather than the global adapter: again,
only the wizard pages are made scrollable.

