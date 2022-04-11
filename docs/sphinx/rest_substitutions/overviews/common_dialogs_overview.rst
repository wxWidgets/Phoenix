.. include:: headings.inc


.. _common dialogs:

===================================
|phoenix_title|  **Common Dialogs**
===================================


Common dialog classes and functions encapsulate commonly-needed dialog
box requirements. They are all 'modal', grabbing the flow of control
until the user dismisses the dialog, to make them easy to use within
an application.

Some dialogs have both platform-dependent and platform-independent
implementations, so that if underlying windowing systems do not
provide the required functionality, the generic classes and functions
can stand in. For example, under MS Windows, :ref:`wx.ColourDialog`
uses the standard colour selector. There is also an equivalent called
`wx.GenericColourDialog` for other platforms, and a macro defines
:ref:`wx.ColourDialog` to be the same as `wx.GenericColourDialog` on
non-MS Windows platforms. However, under MS Windows, the generic
dialog can also be used, for testing or other purposes.



.. _colourdialog overview:

ColourDialog Overview
---------------------

The :ref:`wx.ColourDialog` presents a colour selector to the user, and
returns with colour information.


The MS Windows Colour Selector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Under Windows, the native colour selector common dialog is used. This
presents a dialog box with three main regions: at the top left, a
palette of 48 commonly-used colours is shown. Under this, there is a
palette of 16 'custom colours' which can be set by the application if
desired. Additionally, the user may open up the dialog box to show a
right-hand panel containing controls to select a precise colour, and
add it to the custom colour palette.


The Generic Colour Selector
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Under non-MS Windows platforms, the colour selector is a simulation of
most of the features of the MS Windows selector.  Two palettes of 48
standard and 16 custom colours are presented, with the right-hand area
containing three sliders for the user to select a colour from red,
green and blue components. This colour may be added to the custom
colour palette, and will replace either the currently selected custom
colour, or the first one in the palette if none is selected.  The RGB
colour sliders are not optional in the generic colour selector. The
generic colour selector is also available under MS Windows; use the
name `wx.GenericColourDialog`.


Example
^^^^^^^

Here is an example of using :ref:`wx.ColourDialog`, which sets various
parameters of a :ref:`wx.ColourData` object, including a grey scale
for the custom colours. If the user did not cancel the dialog, the
application retrieves the selected colour and uses it to set the
background of a window::

	data = wx.ColourData()
	data.SetChooseFull(True)

	for i in xrange(16):
	    colour = wx.Colour(i*16, i*16, i*16)
	    data.SetCustomColour(i, colour)

	dialog = wx.ColourDialog(self, data)
	if dialog.ShowModal() == wx.ID_OK:
	    retData = dialog.GetColourData()
	    col = retData.GetColour()
	    brush = wx.Brush(col, wx.SOLID)
	    myWindow.SetBackground(brush)
	    myWindow.Clear()
	    myWindow.Refresh()




.. _fontdialog overview:

FontDialog Overview
-------------------


The :ref:`wx.FontDialog` presents a font selector to the user, and
returns with font and colour information.


The MS Windows Font Selector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Under Windows, the native font selector common dialog is used. This
presents a dialog box with controls for font name, point size, style,
weight, underlining, strikeout and text foreground colour. A sample of
the font is shown on a white area of the dialog box. Note that in the
translation from full MS Windows fonts to wxPython font conventions,
strikeout is ignored and a font family (such as Swiss or Modern) is
deduced from the actual font name (such as Arial or Courier).


The Generic Font Selector
^^^^^^^^^^^^^^^^^^^^^^^^^

Under non-MS Windows platforms, the font selector is simpler. Controls
for font family, point size, style, weight, underlining and text
foreground colour are provided, and a sample is shown upon a white
background. The generic font selector is also available under MS
Windows; use the name `wx.GenericFontDialog`.


Example
^^^^^^^

Here is an example of using :ref:`wx.FontDialog`. The application uses
the returned font and colour for drawing text on a canvas::

	data = wx.FontData()
	data.SetInitialFont(canvasFont)
	data.SetColour(canvasTextColour)

	dialog = wx.FontDialog(self, data)
	if dialog.ShowModal() == wx.ID_OK:
	    retData = dialog.GetFontData()
	    canvasFont = retData.GetChosenFont()
	    canvasTextColour = retData.GetColour()
	    myWindow.Refresh()




.. _printdialog overview:

PrintDialog Overview
--------------------


This class represents the print and print setup common dialogs. You
may obtain a :ref:`wx.PrinterDC` device context from a successfully
dismissed print dialog.

.. seealso:: :ref:`Printing Framework Overview <printing framework overview>`
     for an example.



.. _filedialog overview:

FileDialog Overview
-------------------


Pops up a file selector box. On Windows and GTK 2.4+, this is the
common file selector dialog. In X, this is a file selector box with
somewhat less functionality. The path and filename are distinct
elements of a full file pathname.

If path is "", the current directory will be used. If filename is "",
no default filename will be supplied.  The wildcard determines what
files are displayed in the file selector, and file extension supplies
a type extension for the required filename. Flags may be a combination
of ``wx.FD_OPEN``, ``wx.FD_SAVE``, ``wx.FD_OVERWRITE_PROMPT``,
``wx.FD_HIDE_READONLY``, ``wx.FD_FILE_MUST_EXIST``, ``wx.FD_MULTIPLE``,
``wx.FD_CHANGE_DIR`` or 0.

Both the X and Windows versions implement a wildcard filter. Typing a
filename containing wildcards ``(\*, ?)`` in the filename text item,
and clicking on Ok, will result in only those files matching the
pattern being displayed. In the X version, supplying no default name
will result in the wildcard filter being inserted in the filename text
item; the filter is ignored if a default name is supplied.

The wildcard may be a specification for multiple types of file with a
description for each, such as::

    wildcard = "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif"



.. _dirdialog overview:

DirDialog Overview
-------------------


This dialog shows a directory selector dialog, allowing the user to
select a single directory.



.. _textentrydialog overview:

TextEntryDialog Overview
------------------------

This is a dialog with a text entry field. The value that the user
entered is obtained using :meth:`wx.TextEntryDialog.GetValue` ().



.. _passwordentrydialog overview:

PasswordEntryDialog Overview
----------------------------

This is a dialog with a password entry field. The value that the user
entered is obtained using :meth:`wx.TextEntryDialog.GetValue` ().



.. _messagedialog overview:

MessageDialog Overview
----------------------

This dialog shows a message, plus buttons that can be chosen from
``OK``, ``Cancel``, ``Yes``, and ``No``. Under Windows, an optional
icon can be shown, such as an exclamation mark or question mark.

The return value of :meth:`wx.MessageDialog.ShowModal` () indicates
which button the user pressed.



.. _singlechoicedialog overview:

SingleChoiceDialog Overview
---------------------------

This dialog shows a list of choices, plus ``OK`` and (optionally)
``Cancel``. The user can select one of them. The selection can be
obtained from the dialog as an index, a string or client data.



.. _multichoicedialog overview:

MultiChoiceDialog Overview
---------------------------

This dialog shows a list of choices, plus ``OK`` and (optionally)
``Cancel``. The user can select one or more of them.

