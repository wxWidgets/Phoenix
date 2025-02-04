# Name:         viewer.py
# Package:      wx.lib.pdfviewer
#
# Purpose:      A PDF report viewer class
#
# Author:       David Hughes     dfh@forestfield.co.uk
# Copyright:    Forestfield Software Ltd
# Licence:      Same as wxPython host

# History:      Created 17 Jun 2009
#
#               08 Oct 2011, Michael Hipp    michael@redmule.com
#               Added prompt, printer_name, orientation options to
#               pdfViewer.Print(). Added option to pdfViewer.LoadFile() to
#               accept a file-like object as well as a path string
#
# Tags:         phoenix-port, documented, unittest
#
#----------------------------------------------------------------------------

"""

This module provides the :class:`~wx.lib.pdfviewer.viewer.pdfViewer` to view PDF
files.
"""
import bisect
import itertools
import copy
import shutil
from io import BytesIO

import wx

VERBOSE = True

try:
    # see http://pythonhosted.org/PyMuPDF - documentation & installation
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    mupdf = True
    if VERBOSE: print('pdfviewer using PyMuPDF (GPL)')
except ImportError:
    mupdf = False
    try:
        # see http://pythonhosted.org/PyPDF2
        import PyPDF2
        from PyPDF2 import PdfFileReader
        from PyPDF2.pdf import ContentStream, PageObject
        from PyPDF2.filters import ASCII85Decode, FlateDecode
        if VERBOSE: print('pdfviewer using PyPDF2')
    except ImportError:
        msg = "PyMuPDF or PyPDF2 must be available to use pdfviewer"
        raise ImportError(msg)

GraphicsContext = wx.GraphicsContext
have_cairo = False
if not mupdf:
    try:
        import wx.lib.wxcairo as wxcairo
        import cairo
        from wx.lib.graphics import GraphicsContext
        have_cairo = True
        if VERBOSE: print('pdfviewer using Cairo')
    except ImportError:
        if VERBOSE: print('pdfviewer using wx.GraphicsContext')

    # New PageObject method added by Forestfield Software
    def extractOperators(self):
        """
        Locate and return all commands in the order they
        occur in the content stream
        """
        ops = []
        content = self["/Contents"].getObject()
        if not isinstance(content, ContentStream):
            content = ContentStream(content, self.pdf)
        for op in content.operations:
            if type(op[1] == bytes):
                op = (op[0], op[1].decode())
            ops.append(op)
        return ops
    # Inject this method into the PageObject class
    PageObject.extractOperators = extractOperators

    # If reportlab is installed, use its stringWidth metric. For justifying text,
    # where widths are cumulative, dc.GetTextExtent consistently underestimates,
    # possibly because it returns integer rather than float.
    try:
        from reportlab.pdfbase.pdfmetrics import stringWidth
        have_rlwidth = True
        if VERBOSE: print('pdfviewer using reportlab stringWidth function')
    except ImportError:
        have_rlwidth = False

#----------------------------------------------------------------------------

class pdfViewer(wx.ScrolledWindow):
    """
    View pdf file in a scrolled window.  Contents are read from PDF file
    and rendered in a GraphicsContext. Show visible window contents
    as quickly as possible then, when using pyPDF, read the whole file and build
    the set of drawing commands for each page. This can take time for a big file or if
    there are complex drawings eg. ReportLab's colour shading inside charts and a
    progress bar can be displayed by setting self.ShowLoadProgress = True (default)
    """
    def __init__(self, parent, nid, pos, size, style):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `nid`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style (unused);

        """
        wx.ScrolledWindow.__init__(self, parent, nid, pos, size,
                                style | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)     # recommended in wxWidgets docs
        self.buttonpanel = None     # reference to panel is set by their common parent
        self._showLoadProgress = (not mupdf)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.have_file = False
        self.resizing = False
        self.numpages = None
        self.zoomscale = -1     # fit page to screen width
        self.nom_page_gap = 20  # nominal inter-page gap (points)
        self.scrollrate = 20    # pixels per scrollbar increment
        self.page_buffer_valid = False
        self.page_after_zoom_change = None
        self.ClearBackground()

    def OnIdle(self, event):
        """
        Redraw on resize.
        """
        if self.resizing:
            self.page_buffer_valid = False
            self.Render()
            self.resizing = False
        event.Skip()

    def OnResize(self, event):
        """
        Buffer size change due to client area resize.
        """
        self.resizing = True
        event.Skip()

    def OnScroll(self, event):
        """
        Recalculate and redraw visible area. CallAfter is *essential*
        for coordination.
        """
        wx.CallAfter(self.Render)
        event.Skip()

    def OnPaint(self, event):
        """
        Refresh visible window with bitmap contents.
        """
        paintDC = wx.PaintDC(self)
        paintDC.Clear()         # in case buffer now smaller than visible window
        if hasattr(self, 'pdc'):
            paintDC.Blit(0, 0, self.winwidth, self.winheight, self.pdc,
                                                     self.xshift, self.yshift)

#----------------------------------------------------------------------------

    # This section defines the externally callable methods:
    # LoadFile, Save, Print, SetZoom, and GoPage
    # also the getter and setter for ShowLoadProgress
    # that is only applicable if using PyPDF2

    def LoadFile(self, pdf_file):
        """
        Read pdf file. Assume all pages are same size, for now.

        :param `pdf_file`: can be either a string holding
        a filename path or a file-like object.
        """
        def create_fileobject(filename):
            """
            Create and return a file object with the contents of filename,
            only used for testing.
            """
            with open(filename, 'rb') as f:
                stream = f.read()
            return BytesIO(stream)

        self.pdfpathname = ''
        if isinstance(pdf_file, str):
            # a filename/path string, save its name
            self.pdfpathname = pdf_file
            # remove comment from next line to test using a file-like object
            # pdf_file = create_fileobject(pdf_file)
        if mupdf:
            self.pdfdoc = mupdfProcessor(self, pdf_file)
        else:
            self.pdfdoc = pypdfProcessor(self, pdf_file, self.ShowLoadProgress)

        self.numpages = self.pdfdoc.numpages
        self.pagesizes = [self.pdfdoc.GetPageSize(i) for i in range(self.numpages)]
        
        self.page_buffer_valid = False
        self.Scroll(0, 0)               # in case this is a re-LoadFile
        self.CalculateDimensions()      # to get initial visible page range
        # draw and display the minimal set of pages
        self.pdfdoc.DrawFile(self.frompage, self.topage)
        self.have_file = True
        # now draw full set of pages
        wx.CallAfter(self.pdfdoc.DrawFile, 0, self.numpages-1)

    def Save(self):
        "Save a copy of the pdf file if it was originally named"
        if self.pdfpathname:
            wild = "Portable document format (*.pdf)|*.pdf"
            dlg = wx.FileDialog(self, message="Save file as ...",
                                  wildcard=wild, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() == wx.ID_OK:
                pathname = dlg.GetPath()
                shutil.copy(self.pdfpathname, pathname)
            dlg.Destroy()

    def Print(self, prompt=True, printer_name=None, orientation=None):
        """
        Print the pdf.

        :param boolean `prompt`: show the print dialog to the user (True/False). If
         False, the print dialog will not be shown and the pdf will be printed
         immediately. Default: True.
        :param string `printer_name`: the name of the printer that is to
         receive the printout. Default: as set by the O/S.
        :param `orientation`: select the orientation (:class:`wx.PORTRAIT` or
         :class:`wx.LANDSCAPE`) for the printout. Default: as set by the O/S.
        """
        pdd = wx.PrintDialogData()
        pdd.SetMinPage(1)
        pdd.SetFromPage(1)
        pdd.SetMaxPage(self.numpages)
        pdd.SetToPage(self.numpages)
        pdata = pdd.GetPrintData()
        if printer_name:
            pdata.SetPrinterName(printer_name)
        if orientation:
            pdata.SetOrientation(orientation)
        # PrintData does not return actual PrintQuality - it can't as printer_name not known
        # but it defaults to wx.PRINT_QUALITY_HIGH, overriding user's own setting for the
        # printer. However calling SetQuality with a value of 0 seems to leave the printer
        # setting untouched
        pdata.SetQuality(0)
        printer = wx.Printer(pdd)
        printout = pdfPrintout('', self)
        if (not printer.Print(self, printout, prompt=prompt) and
                       printer.GetLastError() == wx.PRINTER_ERROR):
            dlg = wx.MessageDialog(self, 'Unable to perform printing',
                              'Printer' , wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        printout.Destroy()

    def SetZoom(self, zoomscale):
        """
        Positive integer or floating zoom scale will render the file at corresponding
        size where 1.0 is "actual" point size (1/72").
        -1 fits page width and -2 fits page height into client area
        Redisplay the current page(s) at the new size

        :param `zoomscale`: an integer or float

        """
        pagenow = self.frompage
        self.zoomscale = zoomscale
        self.page_buffer_valid = False
        # calling GoPage now will trigger rendering at the new size but the page location
        # will be calculated based on the old zoom scale - so save the required page number
        # and call GoPage again *after* rendering at the new size
        self.page_after_zoom_change = pagenow
        self.GoPage(pagenow)

    def GoPage(self, pagenum):
        """
        Go to page

        :param integer `pagenum`: go to the provided page number if it is valid

        """
        # calling Scroll sometimes doesn't raise wx.EVT_SCROLLWIN eg Windows 8 64 bit - so
        wx.CallAfter(self.Render)

        if not hasattr(self, "cumYpagespixels"):
            return False # This could happen if the file is still loading
        
        if pagenum > 0 and pagenum <= self.numpages:
            self.Scroll(0, self.cumYpagespixels[pagenum-1] //
                           self.GetScrollPixelsPerUnit()[1])
            return True
        else:
            self.Scroll(0, 0)
            return False

    @property
    def ShowLoadProgress(self):
        """Property to control if file reading progress is shown (PyPDF2 only)"""
        return self._showLoadProgress

    @ShowLoadProgress.setter
    def ShowLoadProgress(self, flag):
        """Setter for showLoadProgress."""
        self._showLoadProgress = flag

#----------------------------------------------------------------------------

    # This section is concerned with rendering a sub-set of drawing commands on demand

    def CalculateDimensions(self):
        """
        Compute the required buffer sizes to hold the viewed rectangle and
        the range of pages visible. Set self.page_buffer_valid = False if
        the current set of rendered pages changes
        """
        self.frompage = 0
        self.topage = 0
        device_scale = wx.ClientDC(self).GetPPI()[0]/72.0   # pixels per inch/points per inch
        self.font_scale_metrics =  1.0
        self.font_scale_size = 1.0
        # for Windows only with wx.GraphicsContext the rendered font size is too big
        # in the ratio of screen pixels per inch to points per inch
        # and font metrics are too big in the same ratio for both for Cairo and wx.GC
        if wx.PlatformInfo[1] == 'wxMSW':
            self.font_scale_metrics = 1.0 / device_scale
            if not have_cairo:
                self.font_scale_size = 1.0 / device_scale

        clientSize = self.GetClientSize()
        if clientSize.width < 5 or clientSize.height < 5:
            return False # Window is too small to render
        self.winwidth, self.winheight = clientSize
        self.Ypages = [self.pagesizes[pageno][1] + self.nom_page_gap 
                       for pageno in range(self.numpages)]
        if self.zoomscale > 0.0:
            self.scales = [self.zoomscale * device_scale]*self.numpages
        else:
            if int(self.zoomscale) == -1:   # fit width
                self.scales = [self.winwidth / self.pagesizes[pageno][0] 
                               for pageno in range(self.numpages)]
            else:                           # fit page
                self.scales = [self.winheight / self.pagesizes[pageno][1] 
                               for pageno in range(self.numpages)]
        self.Xpagespixels = [int(round(self.pagesizes[pageno][0] * self.scales[pageno]))
                             for pageno in range(self.numpages)]

        self.Ypagespixels = [None]*self.numpages
        self.page_gaps = [None]*self.numpages
        for pageno in range(self.numpages):
            Ypagepixels = int(round(self.Ypages[pageno] * self.scales[pageno]))
            # adjust Ypagespixels (total number of vertical pixels per page including bottom
            # inter-page gap so Ypagepixels is a whole number of scroll increments and pages
            # change precisely on a scroll click
            idiv = Ypagepixels // self.scrollrate
            nlo = idiv * self.scrollrate
            nhi = (idiv + 1) * self.scrollrate
            if nhi - Ypagepixels < Ypagepixels - nlo:
                self.Ypagespixels[pageno] = nhi
            else:
                self.Ypagespixels[pageno] = nlo
            self.page_gaps[pageno] = (self.Ypagespixels[pageno]/self.scales[pageno] -
                                      self.pagesizes[pageno][1])

        self.cumYpagespixels = list(itertools.accumulate(self.Ypagespixels))

        self.maxwidth = max(self.winwidth, 
                            max(self.Xpagespixels[pageno] for pageno in range(self.numpages)))
        self.maxheight = max(self.winheight, self.cumYpagespixels[-1])
        self.SetVirtualSize((self.maxwidth, self.maxheight))
        self.SetScrollRate(self.scrollrate, self.scrollrate)

        xv, yv = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
         
        self.x0, self.y0   = (xv * dx, yv * dy)
        self.frompage = max(bisect.bisect_left(self.cumYpagespixels, self.y0+1), 0)
        self.topage = min(bisect.bisect_right(self.cumYpagespixels, self.y0+self.winheight-1),
                          self.numpages-1)
        if self.frompage > self.topage:
            return False # Nothing to render. Can happen during initialization
        
        self.page_x0 = 0
        self.pagebufferwidth = max(self.Xpagespixels[pageno]
                                   for pageno in range(self.frompage, self.topage+1))
        self.page_y0 = self.cumYpagespixels[self.frompage-1] if self.frompage else 0
        self.pagebufferheight = self.cumYpagespixels[self.topage] - self.page_y0

        # Inform buttonpanel controls of any changes
        if self.buttonpanel:
            self.buttonpanel.Update(self.frompage, self.numpages,
                                      self.scales[self.frompage]/device_scale)
        
        self.xshift = self.x0 - self.page_x0
        self.yshift = self.y0 - self.page_y0
        
        if not self.page_buffer_valid:  # via external setting
            self.cur_frompage = self.frompage
            self.cur_topage = self.topage
        else:   # page range unchanged? whole visible area will always be inside page buffer
            if self.frompage != self.cur_frompage or self.topage != self.cur_topage:
                self.page_buffer_valid = False    # due to page buffer change
                self.cur_frompage = self.frompage
                self.cur_topage = self.topage
                
        return True

    def Render(self):
        """
        Recalculate dimensions as client area may have been scrolled or resized.
        The smallest unit of rendering that can be done is the pdf page. So render
        the drawing commands for the pages in the visible rectangle into a buffer
        big enough to hold this set of pages. Force re-creating the page buffer
        only when client view moves outside it.
        With PyPDF2, use gc.Translate to render each page wrt the pdf origin,
        which is at the bottom left corner of the page.
        """
        if not self.have_file:
            return
        if not self.CalculateDimensions():
            return # Invalid dimensions: Nothing to render
        if not self.page_buffer_valid:
            # Initialize the buffer bitmap.
            self.pagebuffer = wx.Bitmap(self.pagebufferwidth, self.pagebufferheight)
            self.pdc = wx.MemoryDC(self.pagebuffer)     # must persist

            gc = GraphicsContext.Create(self.pdc)       # Cairo/wx.GraphicsContext API

            # white background
            path = gc.CreatePath()
            path.AddRectangle(0, 0,
                                self.pagebuffer.GetWidth(), self.pagebuffer.GetHeight())
            gc.SetBrush(wx.WHITE_BRUSH)
            gc.FillPath(path)

            for pageno in range(self.frompage, self.topage+1):
                scale = self.scales[pageno]
                pagegap = self.page_gaps[pageno]
                self.xpageoffset = 0 - self.x0
                self.ypageoffset = (self.cumYpagespixels[pageno] - self.Ypagespixels[pageno] -
                                    self.page_y0)
    
                gc.PushState()
                if mupdf:
                    gc.Translate(self.xpageoffset, self.ypageoffset)
                    # scaling is done inside RenderPage
                else:

                    gc.Translate(self.xpageoffset, self.ypageoffset +
                                    self.pagesizes[pageno][1]*scale)
                    gc.Scale(scale, scale)
                self.pdfdoc.RenderPage(gc, pageno, scale=scale)
                
                # Show non-page areas as gray
                gc.PushState()
                gc.SetBrush(wx.Brush(self.GetBackgroundColour()))
                gc.SetPen(wx.TRANSPARENT_PEN)
                gc.Scale(1.0, 1.0)
                
                #inter-page gap
                gc.DrawRectangle(0, self.pagesizes[pageno][1]*scale,
                                 self.pagesizes[pageno][0]*scale, pagegap*scale)
                # gap to the right of the page
                extrawidth = self.winwidth - self.Xpagespixels[pageno]
                if extrawidth > 0:
                    gc.DrawRectangle(self.pagesizes[pageno][0]*scale, 0, 
                                     extrawidth, self.Ypagespixels[pageno])
                gc.PopState() # Pop non-page area
        
                gc.PopState() # Pop page area

        self.page_buffer_valid = True
        self.Refresh(0) # Blit appropriate area of new or existing page buffer to screen

        # ensure we stay on the same page after zoom scale is changed
        if self.page_after_zoom_change:
            self.GoPage(self.page_after_zoom_change)
            self.page_after_zoom_change = None

#============================================================================

class mupdfProcessor(object):
    """
    Create an instance of this class to open a PDF file, process the contents of
    each page and render each one on demand using the GPL mupdf library, which is
    accessed via the pymupdf package bindings (version 1.9.1 or later)
    """
    def __init__(self, parent, pdf_file):
        """
        :param `pdf_file`: a File object or an object that supports the standard
        read and seek methods similar to a File object.
        Could also be a string representing a path to a PDF file.
        """
        self.parent = parent
        if isinstance(pdf_file, str):
            # a filename/path string, pass the name to pymupdf.open
            pathname = pdf_file
            self.pdfdoc = pymupdf.open(pathname)
        else:
            # assume it is a file-like object, pass the stream content to pymupdf.open
            # and a '.pdf' extension in pathname to identify the stream type
            pathname = 'fileobject.pdf'
            if pdf_file.tell() > 0:     # not positioned at start
                pdf_file.seek(0)
            stream = bytearray(pdf_file.read())
            self.pdfdoc = pymupdf.open(pathname, stream)

        try:
            self.numpages = self.pdfdoc.page_count
        except AttributeError: # old PyMuPDF version
            self.numpages = self.pdfdoc.pageCount

        self.zoom_error = False     #set if memory errors during render
        
    def GetPageSize(self, pageNum):
        """ Return width, height for the page """
        try:
            page = self.pdfdoc.load_page(pageNum)
        except AttributeError: # old PyMuPDF version
            page = self.pdfdoc.loadPage(pageNum)
        bound = page.bound()
        return bound.width, bound.height
        
    def DrawFile(self, frompage, topage):
        """
        This is a no-op for mupdf. Each page is scaled and drawn on
        demand during RenderPage directly via a call to page.getPixmap()
        """
        self.parent.GoPage(frompage)

    def RenderPage(self, gc, pageno, scale=1.0):
        " Render the set of pagedrawings into gc for specified page "
        try:
            page = self.pdfdoc.load_page(pageno)
        except AttributeError: # old PyMuPDF version
            page = self.pdfdoc.loadPage(pageno)
        matrix = pymupdf.Matrix(scale, scale)
        try:
            try:
                # MUST be keyword arg(s)
                pix = page.get_pixmap(matrix=matrix, alpha=False)
            except AttributeError: # old PyMuPDF version
                pix = page.getPixmap(matrix=matrix, alpha=False)
            bmp = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)
            gc.DrawBitmap(bmp, 0, 0, pix.width, pix.height)
            self.zoom_error = False
        except (RuntimeError, MemoryError):
            if not self.zoom_error:     # report once only
                self.zoom_error = True
                dlg = wx.MessageDialog(self.parent, 'Out of memory. Zoom level too high?',
                              'pdf viewer' , wx.OK |wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()

#============================================================================

class pypdfProcessor(object):
    """
    Create an instance of this class to open a PDF file, process the contents of
    every page using PyPDF2 then render each one on demand
    """
    def __init__(self, parent, fileobj, showloadprogress):
        self.parent = parent
        self.showloadprogress = showloadprogress
        self.pdfdoc = PdfFileReader(fileobj)
        self.numpages = self.pdfdoc.getNumPages()
        self.pagedrawings = {}
        self.unimplemented = {}
        self.formdrawings = {}
        self.page = None
        self.gstate = None
        self.saved_state = None
        self.knownfont = False
        self.progbar = None
        
    def GetPageSize(self, pageNum):
        mediaBox = self.pdfdoc.getPage(pageNum).mediaBox
        return float(mediaBox.getUpperRight_x()), float(mediaBox.getUpperRight_y())

    # These methods interpret the PDF contents as a set of drawing commands

    def Progress(self, ptype, value):
        " This function is called at regular intervals during Drawfile"
        if ptype == 'start':
            pmsg = 'Reading pdf file'
            self.progbar = wx.ProgressDialog('Load file', pmsg, value, None,
                         wx.PD_AUTO_HIDE|
                            wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME)
        elif ptype == 'progress':
            self.progbar.Update(value)
        elif ptype == 'end':
            self.progbar.Destroy()

    def DrawFile(self, frompage, topage):
        """
        Build set of drawing commands from PDF contents. Ideally these could be drawn
        straight into a PseudoDC and the visible section painted directly into
        scrolled window, but we need to be able to zoom and scale the output quickly
        without having to rebuild the drawing commands (slow). So build our
        own command lists, one per page, into self.pagedrawings.
        """
        numpages_generated = 0
        rp = (self.showloadprogress and frompage == 0 and topage == self.numpages-1)
        if rp: self.Progress('start', self.numpages)
        for pageno in range(frompage, topage+1):
            self.gstate = pdfState()    # state is reset with every new page
            self.saved_state = []
            self.page = self.pdfdoc.getPage(pageno)
            numpages_generated += 1
            pdf_fonts = self.FetchFonts(self.page)
            self.pagedrawings[pageno] = self.ProcessOperators(
                                    self.page.extractOperators(), pdf_fonts)
            if rp: self.Progress('progress', numpages_generated)

        if rp: self.Progress('end', None)
        self.parent.GoPage(frompage)

    def RenderPage(self, gc, pageno, scale=None):
        """
        Render the set of pagedrawings
        In a pdf file, bitmaps are treated as being of unit width and height and
        are scaled via a previous ConcatTransform containing the corresponding width
        and height as scale factors. wx.GraphicsContext/Cairo appear not to respond to
        this so scaling is removed from transform and width & height are added
        to the Drawbitmap call.
        """
        drawdict = {'ConcatTransform': gc.ConcatTransform,
                    'PushState': gc.PushState,
                    'PopState': gc.PopState,
                    'SetFont': gc.SetFont,
                    'SetPen': gc.SetPen,
                    'SetBrush': gc.SetBrush,
                    'DrawText': gc.DrawText,
                    'DrawBitmap': gc.DrawBitmap,
                    'CreatePath': gc.CreatePath,
                    'DrawPath': gc.DrawPath }
        for drawcmd, args, kwargs in self.pagedrawings[pageno]:
            # scale font if requested by printer DC
            if drawcmd == 'SetFont' and hasattr(gc, 'font_scale'):
                args[0].Scale(gc.font_scale)
            if drawcmd == 'ConcatTransform':
                cm = gc.CreateMatrix(*args, **kwargs)
                args = (cm,)
            if drawcmd == 'CreatePath':
                gp = drawdict[drawcmd](*args, **kwargs)
                continue
            elif drawcmd == 'DrawPath':
                args = (gp, args[1])
            if drawcmd in drawdict:
                drawdict[drawcmd](*args, **kwargs)
                # reset font scaling in case RenderPage call is repeated
                if drawcmd == 'SetFont' and hasattr(gc, 'font_scale'):
                    args[0].Scale(1.0/gc.font_scale)
            else:
                pathdict = {'MoveToPoint': gp.MoveToPoint,
                            'AddLineToPoint': gp.AddLineToPoint,
                            'AddCurveToPoint': gp.AddCurveToPoint,
                            'AddRectangle': gp.AddRectangle,
                            'CloseSubpath': gp.CloseSubpath }
                if drawcmd in pathdict:
                    pathdict[drawcmd](*args, **kwargs)

    def FetchFonts(self, currentobject):
        " Return the standard fonts in current page or form"
        pdf_fonts = {}
        try:
            fonts = currentobject["/Resources"].getObject()['/Font']
            for key in fonts:
                pdf_fonts[key] = fonts[key]['/BaseFont'][1:]     # remove the leading '/'
        except KeyError:
            pass
        return pdf_fonts

    def ProcessOperators(self, opslist, pdf_fonts):
        """
        Interpret each operation in opslist and return in drawlist.
        """
        drawlist = []
        path = []
        for operand, operator in opslist :
            g = self.gstate
            if operator == 'cm' and operand:        # new transformation matrix
                # some operands need inverting because directions of y axis
                # in pdf and graphics context are opposite
                a, b, c, d, e, f = [float(n) for n in operand]
                drawlist.append(['ConcatTransform', (a, -b, -c, d, e, -f), {}])
            elif operator == 'q':       # save state
                self.saved_state.append(copy.deepcopy(g))
                drawlist.append(['PushState', (), {}])
            elif operator == 'Q':       # restore state
                self.gstate = self.saved_state.pop()
                drawlist.append(['PopState', (), {}])
            elif operator == 'RG':      # Stroke RGB
                rs, gs, bs = [int(float(n)*255) for n in operand]
                g.strokeRGB = wx.Colour(rs, gs, bs)
            elif operator == 'rg':      # Fill RGB
                rf, gf, bf = [int(float(n)*255) for n in operand]
                g.fillRGB = wx.Colour(rf, gf, bf)
            elif operator == 'K':       # Stroke CMYK
                rs, gs, bs = self.ConvertCMYK(operand)
                g.strokeRGB = wx.Colour(rs, gs, bs)
            elif operator == 'k':       # Fill CMYK
                rf, gf, bf = self.ConvertCMYK(operand)
                g.fillRGB = wx.Colour(rf, gf, bf)
            elif operator == 'w':       # Line width
                g.lineWidth = max(float(operand[0]), 1.0)
            elif operator == 'J':       # Line cap
                ix = float(operand[0])
                g.lineCapStyle = {0: wx.CAP_BUTT, 1: wx.CAP_ROUND,
                                              2: wx.CAP_PROJECTING}[ix]
            elif operator == 'j':       # Line join
                ix = float(operand[0])
                g.lineJoinStyle = {0: wx.JOIN_MITER, 1: wx.JOIN_ROUND,
                                              2: wx.JOIN_BEVEL}[ix]
            elif operator == 'd':       # Line dash pattern
                g.lineDashArray = [int(n) for n in operand[0]]
                g.lineDashPhase = int(operand[1])
            elif operator in ('m', 'c', 'l', 're', 'v', 'y', 'h'):    # path defining ops
                path.append([[float(n) for n in operand], operator])
            elif operator in ('b', 'B', 'b*', 'B*', 'f', 'F', 'f*',
                                           's', 'S', 'n'):    # path drawing ops
                drawlist.extend(self.DrawPath(path, operator))
                path = []
            elif operator == 'BT':      # begin text object
                g.textMatrix = [1, 0, 0, 1, 0, 0]
                g.textLineMatrix = [1, 0, 0, 1, 0, 0]
            elif operator == 'ET':      # end text object
                continue
            elif operator == 'Tm':      # text matrix
                g.textMatrix = [float(n) for n in operand]
                g.textLineMatrix = [float(n) for n in operand]
            elif operator == 'TL':      # text leading
                g.leading = float(operand[0])
            #elif operator == 'Tc':     # character spacing
            #    g.charSpacing = float(operand[0])
            elif operator == 'Tw':      # word spacing
                g.wordSpacing = float(operand[0])
            elif operator == 'Ts':      # super/subscript
                g.textRise = float(operand[0])
            elif operator == 'Td':      # next line via offsets
                g.textLineMatrix[4] += float(operand[0])
                g.textLineMatrix[5] += float(operand[1])
                g.textMatrix = copy.copy(g.textLineMatrix)
            elif operator == 'T*':      # next line via leading
                g.textLineMatrix[4] += 0
                g.textLineMatrix[5] -= g.leading if g.leading is not None else 0
                g.textMatrix = copy.copy(g.textLineMatrix)
            elif operator == 'Tf':      # text font
                g.font = pdf_fonts[operand[0]]
                g.fontSize = float(operand[1])
            elif operator == 'Tj':      # show text
                drawlist.extend(self.DrawTextString(
                                       operand[0].original_bytes.decode('latin-1')))
            elif operator == 'Do':      # invoke named XObject
                dlist = self.InsertXObject(operand[0])
                if dlist:               # may be unimplemented decode
                    drawlist.extend(dlist)
            elif operator == 'INLINE IMAGE':    # special pyPdf case + operand is a dict
                dlist = self.InlineImage(operand)
                if dlist:               # may be unimplemented decode
                    drawlist.extend(dlist)
            else:                       # report once
                if operator not in self.unimplemented:
                    if VERBOSE: print('PDF operator %s is not implemented' % operator)
                    self.unimplemented[operator] = 1

        # Fix bitmap transform. Move the scaling from any transform matrix that precedes
        # a DrawBitmap operation into the op itself - the width and height extracted from
        # the bitmap is the size of the original PDF image not the size it is to be drawn
        for k in range(len(drawlist)-1):
            if drawlist[k][0] == 'ConcatTransform' and drawlist[k+1][0] == 'DrawBitmap':
                ctargs = list(drawlist[k][1])
                bmargs = list(drawlist[k+1][1])
                bmargs[2] = -ctargs[3]          # y position
                bmargs[3] = ctargs[0]           # width
                bmargs[4] = ctargs[3]           # height
                ctargs[0] = 1.0
                ctargs[3] = 1.0
                drawlist[k][1] = tuple(ctargs)
                drawlist[k+1][1] = tuple(bmargs)
        return drawlist

    def SetFont(self, pdfont, size):
        """
        Returns :class:`wx.Font` instance from supplied pdf font information.
        """
        self.knownfont = True
        pdfont = pdfont.lower()
        if pdfont.count('courier'):
            family = wx.FONTFAMILY_MODERN
            font = 'Courier New'
        elif pdfont.count('helvetica'):
            family = wx.FONTFAMILY_SWISS
            font = 'Arial'
        elif pdfont.count('times'):
            family = wx.FONTFAMILY_ROMAN
            font = 'Times New Roman'
        elif pdfont.count('symbol'):
            family = wx.FONTFAMILY_DEFAULT
            font = 'Symbol'
        elif pdfont.count('zapfdingbats'):
            family = wx.FONTFAMILY_DEFAULT
            font = 'Wingdings'
        else:
            if VERBOSE: print('Unknown font %s' % pdfont)
            self.knownfont = False
            family = wx.FONTFAMILY_SWISS
            font = 'Arial'

        weight = wx.FONTWEIGHT_NORMAL
        if pdfont.count('bold'):
            weight = wx.FONTWEIGHT_BOLD
        style = wx.FONTSTYLE_NORMAL
        if pdfont.count('oblique') or pdfont.count('italic'):
            style = wx.FONTSTYLE_ITALIC
        return wx.Font(max(1, size), family, style, weight, faceName=font)

    def DrawTextString(self, text):
        """
        Draw a text string. Word spacing only works for horizontal text.

        :param string `text`: the text to draw

        """
        dlist = []
        g = self.gstate
        f0  = self.SetFont(g.font, g.fontSize)
        f0.Scale(self.parent.font_scale_metrics)
        f1  = self.SetFont(g.font, g.fontSize)
        f1.Scale(self.parent.font_scale_size)
        dlist.append(['SetFont', (f1, g.fillRGB), {}])
        if g.wordSpacing > 0:
            textlist = text.split(' ')
        else:
            textlist = [text,]
        for item in textlist:
            dlist.append(self.DrawTextItem(item, f0))
        return dlist

    def DrawTextItem(self, textitem, f):
        """
        Draw a text item.

        :param `textitem`: the item to draw
        :param `f`: the font to use for text extent measuring

        """
        dc = wx.ClientDC(self.parent)      # dummy dc for text extents
        g = self.gstate
        x = g.textMatrix[4]
        y = g.textMatrix[5] + g.textRise
        if g.wordSpacing > 0:
            textitem += ' '
        wid, ht, descend, x_lead = dc.GetFullTextExtent(textitem, f)
        if have_rlwidth and self.knownfont:   # use ReportLab stringWidth if available
            width = stringWidth(textitem, g.font, g.fontSize)
        else:
            width = wid
        g.textMatrix[4] += (width + g.wordSpacing)  # update current x position
        return ['DrawText', (textitem, x, -y-(ht-descend)), {}]

    def DrawPath(self, path, action):
        """
        Stroke and/or fill the defined path depending on operator.
        """
        dlist = []
        g = self.gstate
        acts = {'S':  (1, 0, 0),
                's':  (1, 0, 0),
                'f':  (0, 1, wx.WINDING_RULE),
                'F':  (0, 1, wx.WINDING_RULE),
                'f*': (0, 1, wx.ODDEVEN_RULE),
                'B':  (1, 1, wx.WINDING_RULE),
                'B*': (1, 1, wx.ODDEVEN_RULE),
                'b':  (1, 1, wx.WINDING_RULE),
                'b*': (1, 1, wx.ODDEVEN_RULE),
                'n':  (0, 0, 0) }
        stroke, fill, rule = acts[action]
        if action in ('s', 'b', 'b*'):
            path.append([[], 'h'])      # close path

        if stroke:
            if g.lineDashArray:
                style = wx.PENSTYLE_USER_DASH
            else:
                style = wx.PENSTYLE_SOLID
            cpen = wx.Pen(g.strokeRGB, g.lineWidth, style)
            cpen.SetCap(g.lineCapStyle)
            cpen.SetJoin(g.lineJoinStyle)
            if g.lineDashArray:
                cpen.SetDashes(g.lineDashArray)
            dlist.append(['SetPen', (cpen,), {}])
        else:
            dlist.append(['SetPen', (wx.TRANSPARENT_PEN,), {}])

        if fill:
            dlist.append(['SetBrush', (wx.Brush(g.fillRGB),), {}])
        else:
            dlist.append(['SetBrush', (wx.TRANSPARENT_BRUSH,), {}])

        dlist.append(['CreatePath', (), {}])
        for xylist, op in path:
            if op == 'm':           # move (to) current point
                x0 = xc = xylist[0]
                y0 = yc = -xylist[1]
                dlist.append(['MoveToPoint', (x0, y0), {}])
            elif op == 'l':         # draw line
                x2 = xylist[0]
                y2 = -xylist[1]
                dlist.append(['AddLineToPoint', (x2, y2), {}])
                xc = x2
                yc = y2
            elif op == 're':        # draw rectangle
                x = xylist[0]
                y = -xylist[1]
                w = xylist[2]
                h = xylist[3]
                retuple = (x, y-h, w, h)
                if h < 0.0:
                    retuple = (x, y, w, -h)
                dlist.append(['AddRectangle', retuple, {}])
            elif op in ('c', 'v', 'y'):         # draw Bezier curve
                args = []
                if op == 'v':
                    args.extend([xc, yc])
                args.extend([xylist[0], -xylist[1],
                                xylist[2], -xylist[3]])
                if op == 'y':
                    args.extend([xylist[2], -xylist[3]])
                if op == 'c':
                    args.extend([xylist[4], -xylist[5]])
                dlist.append(['AddCurveToPoint', args, {}])
            elif op == 'h':
                dlist.append(['CloseSubpath', (), {}])
        dlist.append(['DrawPath', ('GraphicsPath', rule), {}])
        return dlist

    def InsertXObject(self, name):
        """
        XObject can be an image or a 'form' (an arbitrary PDF sequence).
        """
        dlist = []
        xobject = self.page["/Resources"].getObject()['/XObject']
        stream = xobject[name]
        if stream.get('/Subtype') == '/Form':
            # insert contents into current page drawing
            if not name in self.formdrawings:       # extract if not already done
                pdf_fonts = self.FetchFonts(stream)
                x_bbox = stream.get('/BBox')
                matrix = stream.get('/Matrix')
                form_ops = ContentStream(stream, self.pdfdoc).operations
                oplist = [([], 'q'), (matrix, 'cm')]    # push state & apply matrix
                oplist.extend(form_ops)                 # add form contents
                oplist.append(([], 'Q'))                # restore original state
                self.formdrawings[name] = self.ProcessOperators(oplist, pdf_fonts)
            dlist.extend(self.formdrawings[name])
        elif stream.get('/Subtype') == '/Image':
            width = stream['/Width']
            height = stream['/Height']
            x_depth = stream['/BitsPerComponent']
            filters = stream["/Filter"]
            item = self.AddBitmap(stream._data, width, height, filters)
            if item:            # may be unimplemented
                dlist.append(item)
        return dlist

    def InlineImage(self, operand):
        """ operand contains an image"""
        dlist = []
        data = operand.get('data')
        settings = operand.get('settings')
        width = settings['/W']
        height = settings['/H']
        x_depth = settings['/BPC']
        filters = settings['/F']
        item = self.AddBitmap(data, width, height, filters)
        if item:            # may be unimplemented
            dlist.append(item)
        return dlist

    def AddBitmap(self, data, width, height, filters):
        """
        Add wx.Bitmap from data, processed by filters.
        """
        if '/A85' in filters or '/ASCII85Decode' in filters:
            data = ASCII85Decode.decode(data)
        if '/Fl' in filters or '/FlateDecode' in filters:
            data = FlateDecode.decode(data, None)
        if '/CCF' in filters or  '/CCITTFaxDecode' in filters:
            if VERBOSE:
                print('PDF operation /CCITTFaxDecode is not implemented')
            return []
        if '/DCT' in filters or '/DCTDecode' in filters:
            stream = BytesIO(data)
            image = wx.Image(stream, wx.BITMAP_TYPE_JPEG)
            bitmap = wx.Bitmap(image)
        else:
            try:
                bitmap = wx.Bitmap.FromBuffer(width, height, data)
            except:
                return []       # any error
        return ['DrawBitmap', (bitmap, 0, 0-height, width, height), {}]

    def ConvertCMYK(self, operand):
        """
        Convert CMYK values (0 to 1.0) in operand to nearest RGB.
        """
        c, m, y, k = operand
        r = round((1-c)*(1-k)*255)
        b = round((1-y)*(1-k)*255)
        g = round((1-m)*(1-k)*255)
        return (r, g, b)

#----------------------------------------------------------------------------

class pdfState(object):
    """
    Instance holds the current pdf graphics and text state. It can be
    saved (pushed) and restored (popped) by the owning parent
    """
    def __init__ (self):
        """
        Creates an instance with default values. Individual attributes
        are modified directly not via getters and setters
        """
        self.lineWidth = 1.0
        self.lineCapStyle = wx.CAP_BUTT
        self.lineJoinStyle = wx.JOIN_MITER
        self.lineDashArray = []
        self.lineDashPhase = 0
        self.miterLimit = None
        self.strokeRGB = wx.BLACK
        self.fillRGB = wx.BLACK  # used for both shapes & text
        self.fillMode = None

        self.textMatrix = [1, 0, 0, 1, 0, 0]
        self.textLineMatrix = [1, 0, 0, 1, 0, 0]
        self.charSpacing = 0
        self.wordSpacing = 0
        self.horizontalScaling = None
        self.leading = None
        self.font = None
        self.fontSize = None
        self.textRenderMode = None
        self.textRise = 0

#------------------------------------------------------------------------------

class pdfPrintout(wx.Printout):
    """
    Class encapsulating the functionality of printing out the document. The methods below
    over-ride those of the base class and supply document-specific information to the
    printing framework that calls them internally.
    """
    def __init__(self, title, view):
        """
        Pass in the instance of dpViewer to be printed.
        """
        wx.Printout.__init__(self, title)
        self.view = view

    def HasPage(self, pageno):
        """
        Report whether pageno exists.
        """
        if pageno <= self.view.numpages:
            return True
        else:
            return False

    def GetPageInfo(self):
        """
        Supply maximum range of pages and the range to be printed
        These are initial values passed to Printer dialog, where they
        can be amended by user.
        """
        maxnum = self.view.numpages
        return (1, maxnum, 1, maxnum)

    def OnPrintPage(self, page):
        """
        Provide the data for page by rendering the drawing commands
        to the printer DC, MuPDF returns the page content from an internally
        generated bitmap and sfac sets it to a high enough resolution that
        reduces anti-aliasing blur but keeps it small to minimise printing time
        """
        sfac = 1.0
        if mupdf:
            sfac = 4.0
        pageno = page - 1       # zero based
        width = self.view.pagesizes[pageno][0]
        height = self.view.pagesizes[pageno][1]
        self.FitThisSizeToPage(wx.Size(int(width*sfac), int(height*sfac)))
        dc = self.GetDC()
        gc = wx.GraphicsContext.Create(dc)
        if not mupdf:
            gc.Translate(0, height)
        if wx.PlatformInfo[1] == 'wxMSW' and have_cairo:
            device_scale = wx.ClientDC(self.view).GetPPI()[0]/72.0   # pixels per inch/ppi
            gc.font_scale = 1.0 / device_scale

        self.view.pdfdoc.RenderPage(gc, pageno, sfac)
        return True
