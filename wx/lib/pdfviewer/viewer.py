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
# Tags:        phoenix-port, documented, unittest
#
#----------------------------------------------------------------------------
"""
This module provides the :class:`~lib.pdfviewer.viewer.pdfViewer` to view PDF
files.
"""

import sys
import os
import time
import types
import copy
import shutil

from wx.lib.six import BytesIO

USE_CAIRO = True
FONTSCALE = 1.0
CACHE_LATE_PAGES = True
LATE_THRESHOLD = 200        # Time to render (ttr), milliseconds

VERBOSE = False

fpypdf = 0
try:
    import pyPdf
    fpypdf = 1
except:
    pass

try:
    import PyPDF2
    fpypdf = 2
except:
    pass

if not fpypdf:
    msg = "You either need pyPdf or pyPDF2 to use this."
    raise ImportError(msg)
elif fpypdf == 2:
    from PyPDF2 import PdfFileReader
    from PyPDF2.pdf import ContentStream, PageObject
    from PyPDF2.filters import ASCII85Decode, FlateDecode
elif fpypdf == 1:
    from pyPdf import PdfFileReader
    from pyPdf.pdf import ContentStream, PageObject
    from pyPdf.filters import ASCII85Decode, FlateDecode

from dcgraphics import dcGraphicsContext

import wx
have_cairo = False
if USE_CAIRO and wx.VERSION_STRING > '2.8.10.1':      # Cairo DrawBitmap bug fixed
    try:
        import cairo
        from wx.lib.graphics import GraphicsContext
        FONTSCALE = 1.0
        have_cairo = True
        if VERBOSE: print('Using Cairo')
    except ImportError:
        pass
if not have_cairo:    
    GraphicsContext = wx.GraphicsContext
    if wx.PlatformInfo[1] == 'wxMSW':   # for Windows only    
        FONTSCALE = 72.0 / 96.0         # wx.GraphicsContext fonts are too big in the ratio
                                        # of screen pixels per inch to points per inch 
    if VERBOSE: print('Using wx.GraphicsContext')

""" If reportlab is installed, use its stringWidth metric. For justifying text,
    where widths are cumulative, dc.GetTextExtent consistently underestimates,
    possibly because it returns integer rather than float.
"""
try:
    from reportlab.pdfbase.pdfmetrics import stringWidth
    have_rlwidth = True
except ImportError:
    have_rlwidth = False

#----------------------------------------------------------------------------

## New PageObject method added by Forestfield Software
def extractOperators(self):
    """
    Locate and return all commands in the order they
    occur in the content stream. Used by pdfviewer.
    """
    ops = []
    content = self["/Contents"].getObject()
    if not isinstance(content, ContentStream):
        content = ContentStream(content, self.pdf)
    for op in content.operations:
        ops.append(op)
    return ops

# Inject this method into the PageObject class
PageObject.extractOperators = extractOperators

#----------------------------------------------------------------------------
    
class pdfViewer(wx.ScrolledWindow):
    """ 
    View PDF report files in a scrolled window.  Contents are read from PDF file
    and rendered in a :class:`GraphicsContext`. Show visible window contents
    as quickly as possible then read the whole file and build the set of drawing
    commands for each page. This can take time for a big file or if there are complex
    drawings eg. ReportLab's colour shading inside charts. Originally read in a thread
    but navigation is limited until whole file is ready, so now done in main
    thread with a progress bar, which isn't modal so can still do whatever navigation
    is possible as the content availability increases.
    """
    def __init__(self, parent, id, pos, size, style):
        """
        Default class constructor.

        :param Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`Size`
        :param integer `style`: the button style (unused);

        """
        wx.ScrolledWindow.__init__(self, parent, id, pos, size,
                                style | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)     # recommended in wxWidgets docs
        self.buttonpanel = None     # reference to panel is set by their common parent
        self._showLoadProgress = True
        self._usePrintDirect = True
        
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
        self.ClearBackground()

    def OnIdle(self, event):
        """
        Redraw on resize.
        """
        if self.resizing:
            self.Render()
            self.resizing = False
        event.Skip()

    def OnResize(self, event):
        """
        Buffer size change due to client area resize.
        """
        self.resizing = True
        self.cachedpages = {}
        event.Skip()

    def OnScroll(self,event):
        """
        Recalculate and redraw visible area. CallAfter is *essential*
        for coordination.
        """
        wx.CallAfter(self.Render, force=False)
        event.Skip()

    def OnPaint(self, event):
        """
        Refresh visible window with bitmap contents.
        """
        paintDC = wx.PaintDC(self)
        if hasattr(self, 'pdc'):
            paintDC.Blit(0, 0, self.winwidth, self.winheight, self.pdc,
                                                     self.xshift, self.yshift)
        else:
            paintDC.Clear()

#----------------------------------------------------------------------------

    "The externally callable methods are: LoadFile, Save, Print, SetZoom, and GoPage" 
        
    def LoadFile(self, pdf_file):
        """
        Read pdf file using pyPdf/pyPDF2. Assume all pages are same size, for now.
        
        :param `pdf_file`: can be either a string holding a filename path or
         a file-like object.
         
        """
        if isinstance(pdf_file, types.StringTypes):
            # it must be a filename/path string, open it as a file
            f = file(pdf_file, 'rb')
            self.pdfpathname = pdf_file
        else:
            # assume it is a file-like object
            f = pdf_file
            self.pdfpathname = ''  # empty default file name
        self.pdfdoc = PdfFileReader(f)
        self.numpages = self.pdfdoc.getNumPages()
        page1 = self.pdfdoc.getPage(0)
        self.pagewidth = float(page1.mediaBox.getUpperRight_x())
        self.pageheight = float(page1.mediaBox.getUpperRight_y())
        self.Scroll(0,0)                # in case this is a re-LoadFile
        self.CalculateDimensions(True)  # to get initial visible page range
        self.unimplemented = {}
        self.pagedrawings = {}
        self.formdrawings = {}
        self.cachedpages = {}
        # draw and display the minimal set of pages
        self.DrawFile(self.frompage, self.topage)
        self.have_file = True
        # now draw full set of pages
        wx.CallAfter(self.DrawFile, 0, self.numpages-1)

    def Save(self):
        """
        A pdf-only Save.
        """
        wild = "Portable document format (*.pdf)|*.pdf"
        dlg = wx.FileDialog(self, message="Save file as ...",
                                  wildcard=wild,
                                  style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
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
        Positive integer or floating zoom scale will render the file at
        the corresponding size where 1.0 is "actual" point size (1/72"). 
        -1 fits page width and -2 fits page height into client area
        Redisplay the current page(s) at the new size
        
        :param `zoomscale`: an integer or float
        
        """
        pagenow = self.frompage
        self.zoomscale = zoomscale
        self.cachedpages = {}
        self.CalculateDimensions(True)
        self.GoPage(pagenow)

    def GoPage(self, pagenum):
        """
        Go to page
        
        :param integer `pagenum`: go to the provided page number if it is valid
        
        """
        if pagenum > 0 and pagenum <= self.numpages:
            self.Scroll(0, pagenum*self.Ypagepixels/self.GetScrollPixelsPerUnit()[1])
        else:
            self.Scroll(0, 0)
            self.Render()

#----------------------------------------------------------------------------

    "This section is concerned with rendering a sub-set of drawing commands on demand"

    def CalculateDimensions(self, force):
        """
        Compute the required buffer sizes to hold the viewed rectangle and
        the range of pages visible. Override force flag and set true if 
        the current set of rendered pages changes.
        """
        self.frompage = 0
        self.topage = 0
        self.clientdc = dc = wx.ClientDC(self)      # dc for device scaling 
        self.device_scale = dc.GetPPI()[0]/72.0     # pixels per inch / points per inch 
        self.winwidth, self.winheight = self.GetClientSize()
        if self.winheight < 100:
            return
        self.Ypage = self.pageheight + self.nom_page_gap
        if self.zoomscale > 0.0:
            self.scale = self.zoomscale * self.device_scale
        else:
            if int(self.zoomscale) == -1:   # fit width
                self.scale = self.winwidth / self.pagewidth
            else:                           # fit page
                self.scale = self.winheight / self.pageheight
        self.Xpagepixels = int(round(self.pagewidth*self.scale))
        self.Ypagepixels = int(round(self.Ypage*self.scale))

        # adjust inter-page gap so Ypagepixels is a whole number of scroll increments
        # and page numbers change precisely on a scroll click
        idiv = self.Ypagepixels/self.scrollrate
        nlo = idiv * self.scrollrate
        nhi = (idiv + 1) * self.scrollrate
        if nhi - self.Ypagepixels < self.Ypagepixels - nlo:
            self.Ypagepixels = nhi
        else:
            self.Ypagepixels = nlo
        self.page_gap = self.Ypagepixels/self.scale - self.pageheight   

        self.maxwidth = max(self.winwidth, self.Xpagepixels)
        self.maxheight = max(self.winheight, self.numpages*self.Ypagepixels)
        self.SetVirtualSize((self.maxwidth, self.maxheight))
        self.SetScrollRate(self.scrollrate,self.scrollrate)

        xv, yv = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        self.x0, self.y0   = (xv * dx, yv * dy)
        self.frompage = min(self.y0/self.Ypagepixels, self.numpages-1)
        self.topage = min((self.y0+self.winheight-1)/self.Ypagepixels, self.numpages-1)
        self.pagebufferwidth = max(self.Xpagepixels, self.winwidth)
        self.pagebufferheight = (self.topage - self.frompage + 1) * self.Ypagepixels

        # Inform buttonpanel controls of any changes
        if self.buttonpanel:
            self.buttonpanel.Update(self.frompage, self.numpages,
                                      self.scale/self.device_scale)

        self.page_y0 = self.frompage * self.Ypagepixels
        self.page_x0 = 0
        self.xshift = self.x0 - self.page_x0
        self.yshift = self.y0 - self.page_y0
        if force:               # by external request 
            self.cur_frompage = self.frompage
            self.cur_topage = self.topage
        else:   # page range unchanged? whole visible area will always be inside page buffer
            if self.frompage != self.cur_frompage or self.topage != self.cur_topage:  
                force = True    # due to page buffer change
                self.cur_frompage = self.frompage
                self.cur_topage = self.topage
        return force

    def Render(self, force=True):
        """
        Recalculate dimensions as client area may have been scrolled or resized.
        The smallest unit of rendering that can be done is the pdf page. So render
        the drawing commands for the pages in the visible rectangle into a buffer
        big enough to hold this set of pages. For each page, use gc.Translate to 
        render wrt the pdf origin, which is at the bottom left corner of the page. 
        Force re-creating the page buffer only when client view moves outside it.
        """
        if not self.have_file:
            return
        force = self.CalculateDimensions(force)
        if force:
            # Initialize the buffer bitmap. 
            self.pagebuffer = wx.Bitmap(self.pagebufferwidth, self.pagebufferheight)
            self.pdc = wx.MemoryDC(self.pagebuffer)     # must persist
            gc = GraphicsContext.Create(self.pdc)       # Cairo/wx.GraphicsContext API
            # white background
            path = gc.CreatePath()
            path.AddRectangle(0, 0, self.pagebuffer.GetWidth(), self.pagebuffer.GetHeight())
            gc.SetBrush(wx.WHITE_BRUSH)
            gc.FillPath(path)

            for pageno in range(self.frompage, self.topage+1):
                self.xpageoffset = 0 - self.x0
                self.ypageoffset = pageno*self.Ypagepixels - self.page_y0
                if pageno in self.cachedpages:
                    self.pdc.Blit(self.xpageoffset, self.ypageoffset,
                                     self.Xpagepixels, self.Ypagepixels, 
                                       self.cachedpages[pageno], 0, 0)
                else:    
                    t1 = time.time()
                    gc.PushState()
                    gc.Translate(0 - self.x0, pageno*self.Ypagepixels +
                                        self.pageheight*self.scale - self.page_y0)
                    gc.Scale(self.scale, self.scale)
                    self.RenderPage(gc, self.pagedrawings[pageno])
                    # Show inter-page gap
                    gc.SetBrush(wx.Brush(wx.Colour(180, 180, 180)))        #mid grey
                    gc.SetPen(wx.TRANSPARENT_PEN)
                    gc.DrawRectangle(0, 0, self.pagewidth, self.page_gap)
                    gc.PopState()
                    ttr = time.time()-t1 
                    if CACHE_LATE_PAGES and ttr * 1000 > LATE_THRESHOLD:
                        self.CachePage(pageno)      # save page out of buffer
                    #print('Page %d rendered in %.3f seconds' % (pageno+1, ttr))
            gc.PushState()    
            gc.Translate(0-self.x0, 0-self.page_y0)
            self.RenderPageBoundaries(gc)
            gc.PopState()
        self.Refresh(0)     # Blit appropriate area of new or existing page buffer to screen
        #print('Cached pages:', self.cachedpages.keys())
        #self.pagebuffer.SaveFile('pagemap.png', wx.BITMAP_TYPE_PNG)

    def RenderPage(self, gc, pagedrawings):
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
        for drawcmd, args, kwargs in pagedrawings:
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
            else:
                pathdict = {'MoveToPoint': gp.MoveToPoint,
                            'AddLineToPoint': gp.AddLineToPoint,
                            'AddCurveToPoint': gp.AddCurveToPoint,
                            'AddRectangle': gp.AddRectangle,
                            'CloseSubpath': gp.CloseSubpath }
                if drawcmd in pathdict:    
                    pathdict[drawcmd](*args, **kwargs)

    def RenderPageBoundaries(self, gc):
        """
        Show non-page areas in grey.
        """
        gc.SetBrush(wx.Brush(wx.Colour(180, 180, 180)))        #mid grey
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.Scale(1.0, 1.0)
        extrawidth = self.winwidth - self.Xpagepixels
        if extrawidth > 0:
            gc.DrawRectangle(self.winwidth-extrawidth, 0, extrawidth, self.maxheight)
        extraheight = self.winheight - (self.numpages*self.Ypagepixels - self.y0)
        if extraheight > 0:
            gc.DrawRectangle(0, self.winheight-extraheight, self.maxwidth, extraheight)

    def CachePage(self, pageno):
        """
        When page takes a 'long' time to render, save its contents out of
        self.pdc and re-use it to minimise jerky scrolling.
        """
        cachebuffer = wx.Bitmap(self.Xpagepixels, self.Ypagepixels)
        cdc = wx.MemoryDC(cachebuffer)
        cdc.Blit(0, 0, self.Xpagepixels, self.Ypagepixels,
                      self.pdc, self.xpageoffset, self.ypageoffset)
        self.cachedpages[pageno] = cdc
       
#----------------------------------------------------------------------------

    "These methods interpret the PDF contents as a set of drawing commands"

    def Progress(self, ptype, value):
        """
        This function is called at regular intervals during Drawfile.
        """
        if ptype == 'start':
            msg = 'Reading pdf file'
            self.progbar = wx.ProgressDialog('Load file', msg, value, None,  
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
        without having to rebuild the drawing commands (slow). So roll our
        own command lists, one per page, into self.pagedrawings.
        """  
        t0 = time.time()
        numpages_generated = 0
        rp = (self.ShowLoadProgress and frompage == 0 and topage == self.numpages-1)
        if rp: self.Progress('start', self.numpages)
        for self.pageno in range(frompage, topage+1):
            self.gstate = pdfState()    # state is reset with every new page
            self.saved_state = []
            self.page = self.pdfdoc.getPage(self.pageno)
            numpages_generated += 1
            pdf_fonts = self.FetchFonts(self.page)
            self.pagedrawings[self.pageno] = self.ProcessOperators(
                                    self.page.extractOperators(), pdf_fonts)    
            if rp: self.Progress('progress', numpages_generated)

        ## print('Pages %d to %d. %d pages created in %.2f seconds' % (
        ##           frompage, topage, numpages_generated,(time.time()-t0)))
        if rp: self.Progress('end', None)
        self.GoPage(frompage)

    def FetchFonts(self, currentobject):
        """
        Return the standard fonts in current page or form.
        """
        pdf_fonts = {}
        fonts = currentobject["/Resources"].getObject()['/Font']
        for key in fonts:
            pdf_fonts[key] = fonts[key]['/BaseFont'][1:]     # remove the leading '/'
        return pdf_fonts

    def ProcessOperators(self, opslist, pdf_fonts):
        """
        Interpret each operation in opslist and return in drawlist.
        """
        drawlist = []
        path = []
        for operand, operator in opslist :
            g = self.gstate
            if operator == 'cm':        # new transformation matrix
                # some operands need inverting because directions of y axis
                # in pdf and graphics context are opposite
                a, b, c, d, e, f = map(float, operand)
                drawlist.append(['ConcatTransform', (a, -b, -c, d, e, -f), {}])
            elif operator == 'q':       # save state
                self.saved_state.append(copy.deepcopy(g))
                drawlist.append(['PushState', (), {}])
            elif operator == 'Q':       # restore state
                self.gstate = self.saved_state.pop()
                drawlist.append(['PopState', (), {}])
            elif operator == 'RG':      # Stroke RGB
                rs, gs, bs = [int(v*255) for v in map(float, operand)]
                g.strokeRGB = wx.Colour(rs, gs, bs)
            elif operator == 'rg':      # Fill RGB
                rf, gf, bf = [int(v*255) for v in map(float, operand)]
                g.fillRGB = wx.Colour(rf, gf, bf)
            elif operator == 'K':       # Stroke CMYK
                rs, gs, bs = self.ConvertCMYK(operand)
                g.strokeRGB = wx.Colour(rs, gs, bs)
            elif operator == 'k':       # Fill CMYK
                rf, gf, bf = self.ConvertCMYK(operand)
                g.fillRGB = wx.Colour(rf, gf, bf)
            elif operator == 'w':       # Line width
                g.lineWidth = float(operand[0])
            elif operator == 'J':       # Line cap
                ix = float(operand[0])
                g.lineCapStyle = {0: wx.CAP_BUTT, 1: wx.CAP_ROUND,
                                              2: wx.CAP_PROJECTING}[ix]
            elif operator == 'j':       # Line join
                ix = float(operand[0])
                g.lineJoinStyle = {0: wx.JOIN_MITER, 1: wx.JOIN_ROUND,
                                              2: wx.JOIN_BEVEL}[ix]
            elif operator == 'd':       # Line dash pattern
                g.lineDashArray = map(int, operand[0])
                g.lineDashPhase = int(operand[1])
            elif operator in ('m', 'c', 'l', 're', 'v', 'y', 'h'):    # path defining ops
                path.append([map(float, operand), operator])
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
                g.textMatrix = map(float, operand)
                g.textLineMatrix = map(float, operand)
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
                drawlist.extend(self.DrawTextString(operand[0]))
            elif operator == 'Do':      # invoke named XObject
                drawlist.extend(self.InsertXObject(operand[0]))
            elif operator == 'INLINE IMAGE':    # special pyPdf case + operand is a dict
                drawlist.extend(self.InlineImage(operand))
            else:                       # report once
                if operator not in self.unimplemented:
                    if VERBOSE: print('PDF operator %s is not implemented' % operator)
                    self.unimplemented[operator] = 1

        # Fix bitmap transform. Remove the scaling from any transform matrix that precedes
        # a DrawBitmap operation as the scaling is now done in that operation.
        for k in range(len(drawlist)-1):
            if drawlist[k][0] == 'ConcatTransform' and drawlist[k+1][0] == 'DrawBitmap':
                args = list(drawlist[k][1])
                args[0] = 1.0
                args[3] = 1.0
                drawlist[k][1] = tuple(args)
        return drawlist            

    def SetFont(self, pdfont, size):
        """
        Returns :class:`Font` instance from supplied pdf font information.
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
        return wx.Font(max(1,size), family, style, weight, faceName=font)

    def DrawTextString(self, text): 
        """
        Draw a text string. Word spacing only works for horizontal text.
        
        :param string `text`: the text to draw
        
        """
        dlist = []
        g = self.gstate
        f  = self.SetFont(g.font, g.fontSize*FONTSCALE)
        dlist.append(['SetFont', (f, g.fillRGB), {}])
        if g.wordSpacing > 0:
            textlist = text.split(' ')
        else:
            textlist = [text,]
        for item in textlist:
            dlist.append(self.DrawTextItem(item, f))
        return dlist    

    def DrawTextItem(self, textitem, f):
        """
        Draw a text item.
        
        :param `textitem`: the item to draw  ??? what is the type
        :param `f`: the font to use for text extent measuring ???
        
        """
        dc = wx.ClientDC(self)      # dummy dc for text extents 
        g = self.gstate
        x = g.textMatrix[4]
        y = g.textMatrix[5] + g.textRise
        if g.wordSpacing > 0:
            textitem += ' '
        wid, ht, descend, xlead = dc.GetFullTextExtent(textitem, f)
        if have_rlwidth and self.knownfont:   # use ReportLab stringWidth if available 
            width = stringWidth(textitem, g.font, g.fontSize)
        else:
            width = wid/self.device_scale
        g.textMatrix[4] += (width + g.wordSpacing)  # update current x position
        return ['DrawText', (textitem, x, -y-(ht-descend)/self.device_scale), {}]

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
            elif op == 're':        # draw rectangle (x,y at top left)
                x = xylist[0]
                y = -xylist[1]
                w = xylist[2]
                h = xylist[3]
                dlist.append(['AddRectangle', (x, y-h, w, h), {}])
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
                bbox = stream.get('/BBox')
                matrix = stream.get('/Matrix')
                form_ops = ContentStream(stream, self.pdfdoc).operations
                oplist = [([], 'q'), (matrix, 'cm')]    # push state & apply matrix
                oplist.extend(form_ops)                 # add form contents
                oplist.append(([], 'Q'))                # restore original state
                self.formdrawings[name] = self.ProcessOperators(oplist, pdf_fonts)
            dlist.extend(self.formdrawings[name])
        elif stream.get('/Subtype') == '/Image':
            width = stream.get('/Width') 
            height = stream.get('/Height')
            depth = stream.get('/BitsPerComponent')
            filters = stream.get("/Filter", ())
            dlist.append(self.AddBitmap(stream._data, width, height, filters))
        return dlist

    def InlineImage(self, operand):
        """
        Operand contains an image.
        """
        dlist = []
        data = operand.get('data')
        settings = operand.get('settings')
        width = settings['/W'] 
        height = settings['/H']
        depth = settings['/BPC']
        filters = settings['/F']
        dlist.append(self.AddBitmap(data, width, height, filters))
        return dlist

    def AddBitmap(self, data, width, height, filters):
        """
        Add wx.Bitmap from data, processed by filters.
        """
        if '/A85' in filters or '/ASCII85Decode' in filters:
            data = _AsciiBase85DecodePYTHON(data)
        if '/Fl' in filters or '/FlateDecode' in filters:
            data = FlateDecode.decode(data, None)
        if '/DCT' in filters or '/DCTDecode' in filters:
            stream = BytesIO(data)
            image = wx.Image(stream, wx.BITMAP_TYPE_JPEG)
            bitmap = wx.Bitmap(image)
        else:    
            bitmap = wx.BitmapFromBuffer(width, height, data)
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
    
    @property
    def ShowLoadProgress(self):
        """
        Property to control if loading progress be shown.
        """
        return self._showLoadProgress
    
    @ShowLoadProgress.setter
    def ShowLoadProgress(self, flag):
        """
        Setter for showLoadProgress.
        """
        self._showLoadProgress = flag
       
    @property
    def UsePrintDirect(self):
        """
        Property to control to use either Cairo (via a page buffer) or
        dcGraphicsContext.
        """
        return self._usePrintDirect
    
    @UsePrintDirect.setter
    def UsePrintDirect(self, flag):
        """
        Setter for usePrintDirect.
        """
        self._usePrintDirect = flag
 
#----------------------------------------------------------------------------

class pdfState:
    """
    Instance holds the current pdf graphics and text state. It can be
    saved (pushed) and restored (popped) by the owning parent.
    """
    def __init__ (self):
        """
        Creates an instance with default values. Individual attributes 
        are modified directly not via getters and setters.
        """
        self.lineWidth = 1.0
        self.lineCapStyle = wx.CAP_BUTT
        self.lineJoinStyle = wx.JOIN_MITER
        self.lineDashArray = []
        self.lineDashPhase = 0
        self.miterLimit = None
        self.strokeRGB = wx.Colour(0, 0, 0)
        self.fillRGB = wx.Colour(0, 0, 0)       # used for both shapes & text
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
        max = self.view.numpages
        return (1, max, 1, max)

    def OnPrintPage(self, page):
        """
        Provide the data for page by rendering the drawing commands
        to the printer DC using either Cairo (via a page buffer) or
        dcGraphicsContext depending on the self.view.usePrintDirect property.
        """
        if self.view.UsePrintDirect:
            self.PrintDirect(page)
        else:
            self.PrintViaBuffer(page)
        return True    

    def PrintDirect(self, page):
        """
        Provide the data for page by rendering the drawing commands
        to the printer DC using :class:`~lib.pdfviewer.dcgraphics.dcGraphicsContext`.
        """
        pageno = page - 1       # zero based
        width = self.view.pagewidth
        height = self.view.pageheight
        self.FitThisSizeToPage(wx.Size(width, height))
        dc = self.GetDC()
        gc = dcGraphicsContext.Create(dc, height, have_cairo)
        self.view.RenderPage(gc, self.view.pagedrawings[pageno])

    def PrintViaBuffer(self, page):
        """
        Provide the data for page by drawing it as a bitmap to the printer DC
        sfac needs to provide a high enough resolution bitmap for printing that
        reduces anti-aliasing blur but be kept small to minimise printing time .
        """
        sfac = 6.0
        pageno = page - 1       # zero based
        dc = self.GetDC()
        width = self.view.pagewidth*sfac
        height = self.view.pageheight*sfac
        self.FitThisSizeToPage(wx.Size(width, height))
        # Initialize the buffer bitmap. 
        buffer = wx.Bitmap(width, height)
        mdc = wx.MemoryDC(buffer)
        gc = GraphicsContext.Create(mdc)
        # white background
        path = gc.CreatePath()
        path.AddRectangle(0, 0, width, height)
        gc.SetBrush(wx.WHITE_BRUSH)
        gc.FillPath(path)
        gc.Translate(0, height)
        gc.Scale(sfac, sfac)
        self.view.RenderPage(gc, self.view.pagedrawings[pageno])
        dc.DrawBitmap(buffer, 0, 0)

#------------------------------------------------------------------------------

"""
The following has been "borrowed" from  from reportlab.pdfbase.pdfutils,
where it is used for testing, because the equivalent function in pyPdf
fails when attempting to decode an embedded JPEG image.
"""

def _AsciiBase85DecodePYTHON(input):
    """
    Decodes input using ASCII-Base85 coding.

    This is not used - Acrobat Reader decodes for you
    - but a round trip is essential for testing.
    """
    #strip all whitespace
    stripped = ''.join(input.split())
    #check end
    assert stripped[-2:] == '~>', 'Invalid terminator for Ascii Base 85 Stream'
    stripped = stripped[:-2]  #chop off terminator

    #may have 'z' in it which complicates matters - expand them
    stripped = stripped.replace('z','!!!!!')
    # special rules apply if not a multiple of five bytes.
    whole_word_count, remainder_size = divmod(len(stripped), 5)
    #print('%d words, %d leftover' % (whole_word_count, remainder_size))
    #assert remainder_size != 1, 'invalid Ascii 85 stream!'
    cut = 5 * whole_word_count
    body, lastbit = stripped[0:cut], stripped[cut:]

    out = [].append
    for i in xrange(whole_word_count):
        offset = i*5
        c1 = ord(body[offset]) - 33
        c2 = ord(body[offset+1]) - 33
        c3 = ord(body[offset+2]) - 33
        c4 = ord(body[offset+3]) - 33
        c5 = ord(body[offset+4]) - 33

        num = ((85**4) * c1) + ((85**3) * c2) + ((85**2) * c3) + (85*c4) + c5

        temp, b4 = divmod(num,256)
        temp, b3 = divmod(temp,256)
        b1, b2 = divmod(temp, 256)

        assert  num == 16777216 * b1 + 65536 * b2 + 256 * b3 + b4, 'dodgy code!'
        out(chr(b1))
        out(chr(b2))
        out(chr(b3))
        out(chr(b4))

    #decode however many bytes we have as usual
    if remainder_size > 0:
        while len(lastbit) < 5:
            lastbit = lastbit + '!'
        c1 = ord(lastbit[0]) - 33
        c2 = ord(lastbit[1]) - 33
        c3 = ord(lastbit[2]) - 33
        c4 = ord(lastbit[3]) - 33
        c5 = ord(lastbit[4]) - 33
        num = (((85*c1+c2)*85+c3)*85+c4)*85 + (c5
                 +(0,0,0xFFFFFF,0xFFFF,0xFF)[remainder_size])
        temp, b4 = divmod(num,256)
        temp, b3 = divmod(temp,256)
        b1, b2 = divmod(temp, 256)
        assert  num == 16777216 * b1 + 65536 * b2 + 256 * b3 + b4, 'dodgy code!'
        #print('decoding: %d %d %d %d %d -> %d -> %d %d %d %d' % (
        #    c1,c2,c3,c4,c5,num,b1,b2,b3,b4))

        #the last character needs 1 adding; the encoding loses
        #data by rounding the number to x bytes, and when
        #divided repeatedly we get one less
        if remainder_size == 2:
            lastword = chr(b1)
        elif remainder_size == 3:
            lastword = chr(b1) + chr(b2)
        elif remainder_size == 4:
            lastword = chr(b1) + chr(b2) + chr(b3)
        else:
            lastword = ''
        out(lastword)

    #terminator code for ascii 85
    return ''.join(out.__self__)

