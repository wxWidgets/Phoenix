.. include:: headings.inc


.. _dataobject overview:

========================================
|phoenix_title|  **DataObject Overview**
========================================

This overview discusses data transfer through clipboard or drag and
drop. In wxPython, these two ways to transfer data (either between
different applications or inside one and the same) are very similar
which allows to implement both of them using almost the same code -
or, in other words, if you implement drag and drop support for your
application, you get clipboard support for free and vice versa.

At the heart of both clipboard and drag and drop operations lies the
:class:`wx.DataObject` class. The objects of this class (or, to be
precise, classes derived from it) represent the data which is being
carried by the mouse during drag and drop operation or copied to or
pasted from the clipboard. :class:`wx.DataObject` is a "smart" piece of
data because it knows which formats it supports (see `GetFormatCount`
and `GetAllFormats`) and knows how to render itself in any of them
(see `GetDataHere`). It can also receive its value from the outside in
a format it supports if it implements the `SetData` method. Please see
the documentation of this class for more details.

Both clipboard and drag and drop operations have two sides: the source
and target, the data provider and the data receiver. These which may
be in the same application and even the same window when, for example,
you drag some text from one position to another in a word
processor. Let us describe what each of them should do.


The data provider (source) duties
---------------------------------

The data provider is responsible for creating a :class:`wx.DataObject`
containing the data to be transferred. Then it should either pass it
to the clipboard using :meth:`wx.Clipboard.SetData` function or to
:class:`wx.DropSource` and call :meth:`wx.DropSource.DoDragDrop` function.

A small difference is that in the case of clipboard operation, the
application usually knows in advance whether it copies or cuts
(i.e. copies and deletes) data - in fact, this usually depends on
which menu item the user chose.  But for drag and drop it can only
know it after :meth:`wx.DropSource.DoDragDrop` returns (from its return
value).


The data receiver (target) duties
---------------------------------

To receive (paste in usual terminology) data from the clipboard, you
should create a :class:`wx.DataObject` derived class which supports the
data formats you need and pass it as argument to
:meth:`wx.Clipboard.GetData`. If it returns ``False``, no data in (any
of) the supported format(s) is available. If it returns ``True``, the
data has been successfully transferred to :class:`wx.DataObject`.

For drag and drop case, the :meth:`wx.DropTarget.OnData` virtual function
will be called when a data object is dropped, from which the data
itself may be requested by calling :meth:`wx.DropTarget.GetData` method
which fills the data object.

