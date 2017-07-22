# Name:          __init__.py
# Package:      wx.lib.pdfviewer
#
# Purpose:      A PDF file viewer
#
# Author:       David Hughes     dfh@forestfield.co.uk
# Copyright:    Forestfield Software Ltd
# Licence:      Same as wxPython host

# History:      Created 17 Aug 2009
#
# Tags:         phoenix-port, documented
#
#----------------------------------------------------------------------------
"""
:class:`~wx.lib.pdfviewer.viewer.pdfViewer` class is derived from :class:`wx.ScrolledWindow` class
and can display and print PDF files.

Description
===========

The  :class:`~wx.lib.pdfviewer.viewer.pdfViewer` class is derived from :class:`wx.ScrolledWindow`
and can display and print PDF files. The whole file can be scrolled from
end to end at whatever magnification (zoom-level) is specified.

The viewer uses PyMuPDF (version 1.9.2 or later) or PyPDF2.
If neither of them are installed an import error exception will be raised.

PyMuPDF contains the Python bindings for the underlying MuPDF library, a cross platform,
complete PDF rendering library that is GPL licenced.

Further details on PyMuPDF can be found via http://pythonhosted.org/PyMuPDF

PyPDF2 provides a PdfFileReader class that is used to read the content stream of a PDF
file which is subsequently rendered by :class:`~wx.lib.pdfviewer.viewer.pdfViewer` itself.
Please note that this is not a complete implementation of the pdf specification and
will probably fail to display any random file you supply. However it does seem to
satisfactorily render files typically produced by ReportLab using Western languages.
The main limitation is that it doesn't currently support embedded fonts.

Additional details on PyPDF2 can be found via http://pythonhosted.org/PyPDF2

There is an optional :class:`~wx.lib.pdfviewer.buttonpanel.pdfButtonPanel` class, derived from
:class:`~wx.lib.agw.buttonpanel`, that can be placed, for example, at the top of the
scrolled viewer window, and which contains navigation and zoom controls.

Usage
=====

Sample usage::

    import wx
    import wx.lib.sized_controls as sc

    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

    class PDFViewer(sc.SizedFrame):
        def __init__(self, parent, **kwds):
            super(PDFViewer, self).__init__(parent, **kwds)

            paneCont = self.GetContentsPane()
            self.buttonpanel = pdfButtonPanel(paneCont, wx.NewId(),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
            self.buttonpanel.SetSizerProps(expand=True)
            self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition,
                                    wx.DefaultSize,
                                    wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
            self.viewer.UsePrintDirect = False

            self.viewer.SetSizerProps(expand=True, proportion=1)

            # introduce buttonpanel and viewer to each other
            self.buttonpanel.viewer = self.viewer
            self.viewer.buttonpanel = self.buttonpanel


    if __name__ == '__main__':
        import wx.lib.mixins.inspection as WIT
        app = WIT.InspectableApp(redirect=False)


        pdfV = PDFViewer(None, size=(800, 600))
        pdfV.viewer.UsePrintDirect = False

        pdfV.viewer.LoadFile(r'a path to a .pdf file')
        pdfV.Show()

        app.MainLoop()


Alternatively you can drive the viewer from controls in your own application.

Externally callable methods are:

:meth:`~wx.lib.pdfviewer.viewer.pdfViewer.LoadFile`

:meth:`~wx.lib.pdfviewer.viewer.pdfViewer.Save`

:meth:`~wx.lib.pdfviewer.viewer.pdfViewer.Print`

:meth:`~wx.lib.pdfviewer.viewer.pdfViewer.SetZoom`

:meth:`~wx.lib.pdfviewer.viewer.pdfViewer.GoPage`

The viewer renders the pdf file content using Cairo if installed,
otherwise :class:`wx.GraphicsContext` is used. Printing is achieved by writing
directly to a :class:`wx.PrinterDC` and using :class:`wx.Printer`.

The icons used in :class:`~wx.lib.pdfviewer.buttonpanel.pdfButtonPanel` are Free Icons
by Axialis Software: http://www.axialis.com. You can freely use them in any project,
commercially or not, but you must keep the credits of the authors:
"Axialis Team", even if you modify them. See ./bitmaps/ReadMe.txt for further details.

"""

from .viewer import pdfViewer
from .buttonpanel import pdfButtonPanel
