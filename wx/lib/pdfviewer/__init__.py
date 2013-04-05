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
:class:`~lib.pdfviewer.viewer.pdfViewer` class is derived from :class:`ScrolledWindow` class
and can display and print PDF files.

Description
===========

The  :class:`~lib.pdfviewer.viewer.pdfViewer` class is derived from :class:`ScrolledWindow`
and can display and print PDF files. The whole file can be scrolled from
end to end at whatever magnification (zoom-level) is specified.

The viewer uses pyPDF2 or pyPdf, if neither of them are installed an 
import error exception will be thrown.

Additional details on pyPdf can be found:

- home page: http://pybrary.net/pyPdf/
- download: https://pypi.python.org/pypi/pyPdf

Additional details on pyPDF2 can be found:

- home page: http://knowah.github.com/PyPDF2/
- download: https://github.com/knowah/PyPDF2/

There is an optional :class:`~lib.pdfviewer.buttonpanel.pdfButtonPanel` class, derived from 
:class:`~lib.agw.buttonpanel`, that can be placed, for example, at the top of the
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

:meth:`~lib.pdfviewer.viewer.pdfViewer.LoadFile`

:meth:`~lib.pdfviewer.viewer.pdfViewer.Save`

:meth:`~lib.pdfviewer.viewer.pdfViewer.Print`

:meth:`~lib.pdfviewer.viewer.pdfViewer.SetZoom`

:meth:`~lib.pdfviewer.viewer.pdfViewer.GoPage`
  
The viewer renders the pdf file content using Cairo if installed,
otherwise :class:`GraphicsContext` is used. Printing is achieved by writing
directly to a :class:`PrinterDC` and using :class:`Printer`.

Please note that :class:`~lib.pdfviewer.viewer.pdfViewer` is a far from complete
implementation of the pdf specification and will probably fail to display any
random file you supply. However it does seem to be OK with the sort of files
produced by ReportLab that use Western languages. The biggest limitation is
probably that it doesn't (yet?) support embedded fonts and will substitute one
of the standard fonts instead.

The icons used in :class:`~lib.pdfviewer.buttonpanel.pdfButtonPanel` are Free Icons
by Axialis Software: http://www.axialis.com 

You can freely use them in any project or website, commercially or not. 

TERMS OF USE:

You must keep the credits of the authors: "Axialis Team", even if you modify them. 
See ./bitmaps/ReadMe.txt for further details

"""

from viewer import pdfViewer
from buttonpanel import pdfButtonPanel
