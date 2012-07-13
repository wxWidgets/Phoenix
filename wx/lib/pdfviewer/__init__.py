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
#----------------------------------------------------------------------------
"""
wx.lib.pdfviewer

The wx.lib.pdfviewer  pdfViewer class is derived from wx.ScrolledWindow
and can display and print PDF files. The whole file can be scrolled from
end to end at whatever magnification (zoom-level) is specified.

The viewer uses pyPdf to parse the pdf file so it is a requirement that
this must be installed. The pyPdf home page is http://pybrary.net/pyPdf/
and the library can also be downloaded from http://pypi.python.org/pypi/pyPdf/1.12

There is an optional pdfButtonPanel class, derived from wx.lib.buttonpanel,
that can be placed, for example, at the top of the scrolled viewer window,
and which contains navigation and zoom controls. Alternatively you can drive
the viewer from controls in your own application.

Externally callable methods are: LoadFile, Save, Print, SetZoom, and GoPage

viewer.LoadFile(pathname)
        Reads and displays the specified PDF file

viewer.Save()
        Opens standard file dialog to specify save file name

viewer.Print()
        Opens print dialog to choose printing options

viewer.SetZoom(zoomscale)
        zoomscale: positive integer or floating zoom scale to render the file at
        corresponding size where 1.0 is "actual" point size (1/72"). 
        -1 fits page width and -2 fits page height into client area
        Redisplays the current page(s) at the new size

viewer.GoPage(pagenumber)
        Displays specified page 

The viewer renders the pdf file content using Cairo if installed,
otherwise wx.GraphicsContext is used. Printing is achieved by writing
directly to a wx.PrintDC and using wx.Printer.

Please note that pdfviewer is a far from complete implementation of the pdf
specification and will probably fail to display any random file you supply. 
However it does seem to be OK with the sort of files produced by ReportLab that
use Western languages. The biggest limitation is probably that it doesn't (yet?)
support embedded fonts and will substitute one of the standard fonts instead.

The icons used in pdfButtonbar are Free Icons by Axialis Software: http://www.axialis.com 
You can freely use them in any project or website, commercially or not. 
TERMS OF USE:
You must keep the credits of the authors: "Axialis Team", even if you modify them. 
See ./bitmaps/ReadMe.txt for further details

"""

from viewer import pdfViewer
from buttonpanel import pdfButtonPanel
