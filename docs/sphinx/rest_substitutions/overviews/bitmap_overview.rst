.. include:: headings.inc


.. _bitmaps and icons:

===============================================
|phoenix_title|  **Bitmaps and Icons**
===============================================


The :ref:`Bitmap` class encapsulates the concept of a platform-dependent bitmap, either monochrome or colour. 
Platform-specific methods for creating a :ref:`Bitmap` object from an existing file are catered for.

A bitmap created dynamically or loaded from a file can be selected into a memory device context (instance of 
:ref:`MemoryDC`). This enables the bitmap to be copied to a window or memory device context using :meth:`DC.Blit` (), 
or to be used as a drawing surface.

.. seealso:: :ref:`MemoryDC` for an example of drawing onto a bitmap.


All wxPython platforms support XPMs for small bitmaps and icons. 



.. _supported bitmap file formats:

Supported Bitmap File Formats
-----------------------------

The following lists the formats handled on different platforms. Note that missing or partially-implemented 
formats are automatically supplemented by using :ref:`Image` to load the data, and then converting it to :ref:`Bitmap`
form. Note that using :ref:`Image` is the preferred way to load images in wxPython, with the exception of resources
(XPM-files or native Windows resources).


Bitmap
^^^^^^

Under Windows, :ref:`Bitmap` may load the following formats:

- Windows bitmap resource (``BITMAP_TYPE_BMP_RESOURCE``)
- Windows bitmap file (``BITMAP_TYPE_BMP``)
- XPM data and file (``BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`Image` class.


Under wxGTK, :ref:`Bitmap` may load the following formats:

- XPM data and file (``BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`Image` class.


Under wxMotif and wxX11, :ref:`Bitmap` may load the following formats:

- XBM data and file (``BITMAP_TYPE_XBM``)
- XPM data and file (``BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`Image` class.


Icon
^^^^

Under Windows, :ref:`Icon` may load the following formats:

- Windows icon resource (``BITMAP_TYPE_ICO_RESOURCE``)
- Windows icon file (``BITMAP_TYPE_ICO``)
- XPM data and file (``BITMAP_TYPE_XPM``)


Under wxGTK, :ref:`Icon` may load the following formats:

- XPM data and file (``BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`Image` class.


Under wxMotif and wxX11, :ref:`Icon` may load the following formats:

- XBM data and file (``BITMAP_TYPE_XBM``)
- XPM data and file (``BITMAP_TYPE_XPM``)
- All formats that are supported by the :ref:`Image` class.


Cursor
^^^^^^

Under Windows, :ref:`Cursor` may load the following formats:

- Windows cursor resource (``BITMAP_TYPE_CUR_RESOURCE``)
- Windows cursor file (``BITMAP_TYPE_CUR``)
- Windows icon file (``BITMAP_TYPE_ICO``)
- Windows bitmap file (``BITMAP_TYPE_BMP``)


Under wxGTK, :ref:`Cursor` may load the following formats (in addition to stock cursors):

- None (stock cursors only).


Under wxMotif and wxX11, :ref:`Cursor` may load the following formats:

- XBM data and file (``BITMAP_TYPE_XBM``)


