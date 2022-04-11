#!/usr/bin/env python

import wx

try:
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
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,
                                wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.viewer = pdfViewer( self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        loadbutton = wx.Button(self, wx.ID_ANY, "Load PDF file",
                                wx.DefaultPosition, wx.DefaultSize, 0 )
        vsizer.Add(loadbutton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer.Add(vsizer, 1, wx.GROW|wx.ALL, 5)
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
        from wx.lib.msgpanel import MessagePanel
        win = MessagePanel(nb,
                           'This demo requires either the\n'
                           'PyMuPDF see http://pythonhosted.org/PyMuPDF\n'
                           'or\n'
                           'PyPDF2 see http://pythonhosted.org/PyPDF2\n'
                           'package installed.\n',
                           'Sorry', wx.ICON_WARNING)
        return win

overview = """\
<html><body>
<h2>wx.lib.pdfviewer</h2>

The wx.lib.pdfviewer.pdfViewer class is derived from wx.ScrolledWindow
and can display and print PDF files. The whole file can be scrolled from
end to end at whatever magnification (zoom-level) is specified.

<p> The viewer checks for the <b>PyMuPDF</b> then the <b>PyPDF2</b> package.
If neither are installed an import error exception will be raised.

<p>PyMuPDF contains the Python bindings for the underlying MuPDF library, a cross platform,
complete PDF rendering library that is GPL licenced. PyMuPDF version 1.9.2 or later is required.

<p>Further details on PyMuPDF can be found via http://pythonhosted.org/PyMuPDF

<p>PyPDF2 provides a PdfFileReader class that is used to read the content stream of a PDF
file which is subsequently rendered by the viewer itself.
Please note that this is not a complete implementation of the pdf specification and
will probably fail to render any random PDF file you supply. However it does seem to
behave correctly with files that have been produced by ReportLab using Western languages.
The main limitation is that it doesn't currently support embedded fonts.

<p>Additional details on PyPDF2 can be found via http://pythonhosted.org/PyPDF2

<p> There is an optional pdfButtonPanel class, derived from wx.lib.agw.buttonpanel,
that can be placed, for example, at the top of the scrolled viewer window,
and which contains navigation and zoom controls.

<p>Alternatively you can drive the viewer from controls in your own application.
Externally callable methods are: LoadFile, Save, Print, SetZoom, and GoPage.
(See pdfviewer.__init__.py)

<p> The viewer renders the pdf file content using Cairo if installed,
otherwise wx.GraphicsContext is used. Printing is achieved by writing
directly to a wx.PrintDC and using wx.Printer.

</body></html>
"""

#----------------------------------------------------------------------

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


