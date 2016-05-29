.. include:: headings.inc


.. _toolbar overview:

===========================================
|phoenix_title|  **ToolBar Overview**
===========================================

Introduction
------------

The toolbar family of classes allows an application to use toolbars in
a variety of configurations and styles.

The toolbar is a popular user interface component and contains a set
of bitmap buttons or toggles.  A toolbar gives faster access to an
application's facilities than menus, which have to be popped up and
selected rather laboriously.

Instead of supplying one toolbar class with a number of different
implementations depending on platform, wxPython separates out the
classes. This is because there are a number of different toolbar
styles that you may wish to use simultaneously, and also, future
toolbar implementations will emerge which cannot all be shoe-horned
into the one class.

A toolbar might appear as a single row of images under the menubar, or
it might be in a separate frame layout in several rows and
columns. The class handles the layout of the images, unless explicit
positioning is requested.

A tool is a bitmap which can either be a button (there is no 'state',
it just generates an event when clicked) or it can be a toggle. If a
toggle, a second bitmap can be provided to depict the 'on' state; if
the second bitmap is omitted, either the inverse of the first bitmap
will be used (for monochrome displays) or a thick border is drawn
around the bitmap (for colour displays where inverting will not have
the desired result).

The Windows-specific toolbar classes expect 16-colour bitmaps that are
16 pixels wide and 15 pixels high. If you want to use a different
size, call :meth:`wx.ToolBar.SetToolBitmapSize` as the demo shows, before
adding tools to the button bar.  Don't supply more than one bitmap for
each tool, because the toolbar generates all three images (normal,
depressed, and checked) from the single bitmap you give it.