.. include:: headings.inc


.. _bitmaps and icons:

======================================
|phoenix_title|  **Bitmaps and Icons**
======================================


The :ref:`wx.Bitmap` class encapsulates the concept of a
platform-dependent bitmap, either monochrome or colour.
Platform-specific methods for creating a :ref:`wx.Bitmap` object from
an existing file are catered for.

A bitmap created dynamically or loaded from a file can be selected
into a memory device context (an instance of :ref:`wx.MemoryDC`). This
enables the bitmap to be copied to a window or memory device context
using :meth:`wx.DC.Blit`(), or to be used as a drawing surface.

.. seealso:: :ref:`wx.MemoryDC` for an example of drawing onto a bitmap.


All wxPython platforms support XPMs for small bitmaps and icons.



.. _supported bitmap file formats:

Supported Bitmap File Formats
-----------------------------

The following lists the formats handled on different platforms. Note
that missing or partially-implemented formats are automatically
supplemented by using :ref:`wx.Image` to load the data, and then
converting it to :ref:`wx.Bitmap` form. Note that using
:ref:`wx.Image` is the preferred way to load images in wxPython, with
the exception of resources (XPM-files or native Windows resources).


wx.Bitmap
^^^^^^^^^

Under Windows, :ref:`wx.Bitmap` may load the following formats:

- Windows bitmap resource (``wx.BITMAP_TYPE_BMP_RESOURCE``)
- Windows bitmap file (``wx.BITMAP_TYPE_BMP``)
- XPM data and file (``wx.BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`wx.Image` class.


Under wxGTK, :ref:`wx.Bitmap` may load the following formats:

- XPM data and file (``wx.BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`wx.Image` class.


Under wxMotif and wxX11, :ref:`wx.Bitmap` may load the following formats:

- XBM data and file (``wx.BITMAP_TYPE_XBM``)
- XPM data and file (``wx.BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`wx.Image` class.


wx.Icon
^^^^^^^

Under Windows, :ref:`wx.Icon` may load the following formats:

- Windows icon resource (``wx.BITMAP_TYPE_ICO_RESOURCE``)
- Windows icon file (``wx.BITMAP_TYPE_ICO``)
- XPM data and file (``wx.BITMAP_TYPE_XPM``)


Under wxGTK, :ref:`wx.Icon` may load the following formats:

- XPM data and file (``wx.BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`wx.Image` class.



wx.Cursor
^^^^^^^^^

Under Windows, :ref:`wx.Cursor` may load the following formats:

- Windows cursor resource (``wx.BITMAP_TYPE_CUR_RESOURCE``)
- Windows cursor file (``wx.BITMAP_TYPE_CUR``)
- Windows icon file (``wx.BITMAP_TYPE_ICO``)
- Windows bitmap file (``wx.BITMAP_TYPE_BMP``)


Under wxGTK, :ref:`wx.Cursor` may load the following formats (in
addition to stock cursors):

- None (stock cursors only).



