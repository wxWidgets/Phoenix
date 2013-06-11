
import  wx

try:
    import pyPdf
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    havePyPdf = True
except ImportError:
    havePyPdf = False

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        vsizer = wx.BoxSizer( wx.VERTICAL )
        self.buttonpanel = pdfButtonPanel(self, wx.NewId(),
                                wx.DefaultPosition, wx.DefaultSize, 0)  
        vsizer.Add(self.buttonpanel, 0,
                                wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.viewer = pdfViewer( self, wx.NewId(), wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        loadbutton = wx.Button(self, wx.NewId(), "Load PDF file",
                                wx.DefaultPosition, wx.DefaultSize, 0 )
        vsizer.Add(loadbutton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer.Add(vsizer, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5) 
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel

        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, loadbutton)
        
    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.viewer.LoadFile(dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    if havePyPdf:
        win = TestPanel(nb, log)
        return win
    else:
        from Main import MessagePanel
        win = MessagePanel(nb, 
                           'This demo requires the pyPdf package to be installed.\n'
                           'See: http://pybrary.net/pyPdf/', 
                           'Sorry', wx.ICON_WARNING)
        return win

overview = """\
<html><body>
<h2>wx.lib.pdfviewer</h2>

The wx.lib.pdfviewer.pdfViewer class is derived from wx.ScrolledWindow
and can display and print PDF files. The whole file can be scrolled from
end to end at whatever magnification (zoom-level) is specified.

<p> The viewer uses <b>pyPdf</b> to parse the pdf file so it is a requirement that
this must be installed. The pyPdf home page is http://pybrary.net/pyPdf/
and the library can also be downloaded from http://pypi.python.org/pypi/pyPdf/1.12

<p> There is an optional pdfButtonPanel class, derived from wx.lib.agw.buttonpanel,
that can be placed, for example, at the top of the scrolled viewer window,
and which contains navigation and zoom controls.

<p>Alternatively you can drive the viewer from controls in your own application.
Externally callable methods are: LoadFile, Save, Print, SetZoom, and GoPage.
(See pdfviewer.__init__.py)

<p> The viewer renders the pdf file content using Cairo if installed,
otherwise wx.GraphicsContext is used. Printing is achieved by writing
directly to a wx.PrintDC and using wx.Printer.

<p> Please note that pdfviewer is a far from complete implementation of the pdf
specification and will probably fail to display any random file you supply. 
However it does seem to be OK with the sort of files produced by ReportLab that
use Western languages. The biggest limitation is probably that it doesn't (yet?)
support embedded fonts and will substitute one of the standard fonts instead.

</body></html>
"""

#----------------------------------------------------------------------

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


