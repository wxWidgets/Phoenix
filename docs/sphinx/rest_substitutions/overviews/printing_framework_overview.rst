.. include:: headings.inc


.. _printing framework overview:

=================================================
|phoenix_title|  **Printing Framework Overview**
=================================================


The printing framework relies on the application to provide classes
whose member functions can respond to particular requests, such as
'print this page' or 'does this page exist in the document?'. This
method allows wxPython to take over the housekeeping duties of turning
preview pages, calling the print dialog box, creating the printer
device context, and so on: the application can concentrate on the
rendering of the information onto a device context.

In most cases, the only class you will need to derive from is
:ref:`wx.Printout`; all others will be used as-is.

A brief description of each class's role and how they work together follows.


Printout
--------

A document's printing ability is represented in an application by a
derived :ref:`wx.Printout` class. This class prints a page on request,
and can be passed to the Print function of a :ref:`wx.Printer` object to
actually print the document, or can be passed to a :ref:`wx.PrintPreview`
object to initiate previewing. The following code shows how easy it is
to initiate printing, previewing and the print setup dialog, once the
:ref:`wx.Printout` functionality has been defined. Notice the use of
`MyPrintout` for both printing and previewing. All the preview user
interface functionality is taken care of by wxPython::

	if printing:
	    printer = wx.Printer()
	    printout = MyPrintout("My printout")
	    printer.Print(self, printout, True)

	elif preview:
	    # Pass two printout objects: for preview, and possible printing.
	    preview = wx.PrintPreview(MyPrintout(), MyPrintout())
	    frame = wx.PreviewFrame(preview, self, "Demo Print Preview",
	                            wx.Point(100, 100), wx.Size(600, 650))
	    frame.Centre(wx.BOTH)
	    frame.Initialize()
	    frame.Show(True)



:ref:`wx.Printout` assembles the printed page and (using your subclass's
overrides) writes requested pages to a :ref:`wx.DC` that is passed to
it. This :ref:`wx.DC` could be a :ref:`wx.MemoryDC` (for displaying the
preview image on-screen), a :ref:`wx.PrinterDC` (for printing under MSW
and Mac), or a :ref:`wx.PostScriptDC` (for printing under GTK or
generating PostScript output).

If your window classes have a `Draw(dc)` routine to do screen
rendering, your :ref:`wx.Printout` subclass will typically call those
routines to create portions of the image on your printout. Your
:ref:`wx.Printout` subclass can also make its own calls to its :ref:`wx.DC`
to draw headers, footers, page numbers, etc.

The scaling of the drawn image typically differs from the screen to
the preview and printed images. This class provides a set of routines
named `FitThisSizeToXXX()`, `MapScreenSizeToXXX()`, and
`GetLogicalXXXRect`, which can be used to set the user scale and
origin of the Printout's DC so that your class can easily map your
image to the printout without getting into the details of screen and
printer PPI and scaling.


Printer
-------

Class :ref:`wx.Printer` encapsulates the platform-dependent print
function with a common interface. In most cases, you will not need to
derive a class from :ref:`wx.Printer`; simply create a :ref:`wx.Printer`
object in your `Print` function as in the example above.


PrintPreview
------------

Class :ref:`wx.PrintPreview` manages the print preview process. Among
other things, it constructs the DCs that get passed to your
:ref:`wx.Printout` subclass for printing and manages the display of
multiple pages, a zoomable preview image, and so forth.  In most cases
you will use this class as-is, but you can create your own subclass,
for example, to change the layout or contents of the preview window.


PrinterDC
---------

Class :ref:`wx.PrinterDC` is the :ref:`wx.DC` that represents the actual
printed page under MSW and Mac. During printing, an object of this
class will be passed to your derived :ref:`wx.Printout` object to draw
upon. The size of the :ref:`wx.PrinterDC` will depend on the paper
orientation and the resolution of the printer.

There are two important rectangles in printing: the page rectangle
defines the printable area seen by the application, and under MSW and
Mac, it is the printable area specified by the printer. (For
PostScript printing, the page rectangle is the entire page.)  The
inherited function :meth:`wx.DC.GetSize` returns the page size in device
pixels. The point (0,0) on the :ref:`wx.PrinterDC` represents the top
left corner of the page rectangle; that is, the page rect is given by
`Rect(0, 0, w, h)`, where (w,h) are the values returned by `GetSize`.

The paper rectangle, on the other hand, represents the entire paper
area including the non-printable border. Thus, the coordinates of the
top left corner of the paper rectangle will have small negative
values, while the width and height will be somewhat larger than that
of the page rectangle. The :ref:`wx.PrinterDC` -specific function
:meth:`wx.PrinterDC.GetPaperRect` returns the paper rectangle of the
given :ref:`wx.PrinterDC`.


PostScriptDC
------------

Class :ref:`wx.PostScriptDC` is the :ref:`wx.DC` that represents the actual
printed page under GTK and other PostScript printing.  During
printing, an object of this class will be passed to your derived
:ref:`wx.Printout` object to draw upon. The size of the
:ref:`wx.PostScriptDC` will depend upon the :ref:`wx.PrintData` used to
construct it.

Unlike a :ref:`wx.PrinterDC`, there is no distinction between the page
rectangle and the paper rectangle in a :ref:`wx.PostScriptDC`; both
rectangles are taken to represent the entire sheet of paper.


PrintDialog
-----------

Class :ref:`wx.PrintDialog` puts up the standard print dialog, which
allows you to select the page range for printing (as well as many
other print settings, which may vary from platform to platform). You
provide an object of type :ref:`wx.PrintDialogData` to the
:ref:`wx.PrintDialog` at construction, which is used to populate the
dialog.


.. _print data:

PrintData
---------

Class :ref:`wx.PrintData` is a subset of :ref:`wx.PrintDialogData` that is
used (internally) to initialize a :ref:`wx.PrinterDC` or
:ref:`wx.PostScriptDC`. (In fact, a :ref:`wx.PrintData` is a data member of
a :ref:`wx.PrintDialogData` and a :ref:`wx.PageSetupDialogData`).
Essentially, :ref:`wx.PrintData` contains those bits of information from
the two dialogs necessary to configure the :ref:`wx.PrinterDC` or
:ref:`wx.PostScriptDC` (e.g., size, orientation, etc.). You might wish to
create a global instance of this object to provide call-to-call
persistence to your application's print settings.


.. _print dialog data:

PrintDialogData
---------------

Class :ref:`wx.PrintDialogData` contains the settings entered by the user
in the print dialog. It contains such things as page range, number of
copies, and so forth. In most cases, you won't need to access this
information; the framework takes care of asking your :ref:`wx.Printout`
derived object for the pages requested by the user.


PageSetupDialog
---------------

Class :ref:`wx.PageSetupDialog` puts up the standard page setup dialog,
which allows you to specify the orientation, paper size, and related
settings. You provide it with a :ref:`wx.PageSetupDialogData` object at
initialization, which is used to populate the dialog; when the dialog
is dismissed, this object contains the settings chosen by the user,
including orientation and/or page margins.


.. note:: Note that on Macintosh, the native page setup dialog does
   not contain entries that allow you to change the page margins.



PageSetupDialogData
-------------------

Class :ref:`wx.PageSetupDialogData` contains settings affecting the page
size (paper size), orientation, margins, and so forth. Note that not
all platforms populate all fields; for example, the MSW page setup
dialog lets you set the page margins while the Mac setup dialog does
not.

You will typically create a global instance of each of a
:ref:`wx.PrintData` and :ref:`wx.PageSetupDialogData` at program initiation,
which will contain the default settings provided by the system. Each
time the user calls up either the :ref:`wx.PrintDialog` or the
:ref:`wx.PageSetupDialog`, you pass these data structures to initialize
the dialog values and to be updated by the dialog.  The framework then
queries these data structures to get information like the printed page
range (from the :ref:`wx.PrintDialogData`) or the paper size and/or page
orientation (from the :ref:`wx.PageSetupDialogData`).
