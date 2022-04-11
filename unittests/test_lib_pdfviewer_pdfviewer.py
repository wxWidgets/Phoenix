import unittest
from unittests import wtc
import wx
import os

import wx.lib.sized_controls as sc
try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    havePyPDF = True
except ImportError:
    havePyPDF = False  # Assume neither PyMuPDF nor PyPDF2 found

dataDir = os.path.join(os.path.dirname(__file__), "data")
samplePdf = os.path.join(dataDir, "sample.pdf")

#---------------------------------------------------------------------------

@unittest.skipIf('wxMac' in wx.PlatformInfo or 'wxGTK' in wx.PlatformInfo,
                 'test is crashing on Mac and GTK...')
class lib_pdfviewer_pdfviewer_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(not havePyPDF, "PyMuPDF or PyPDF2 required")
    def test_lib_pdfviewer_pdfviewerButtonPanelCtor(self):
        bp = pdfButtonPanel(self.frame, wx.ID_ANY,
                            wx.DefaultPosition, wx.DefaultSize, 0)

    @unittest.skipIf(not havePyPDF,  "PyMuPDF or PyPDF2 required")
    def test_lib_pdfviewer_pdfviewerPdfViewerCtor(self):
        pv = pdfViewer(self.frame, wx.ID_ANY, wx.DefaultPosition,
                       wx.DefaultSize,
                       wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)

    @unittest.skipIf(not havePyPDF,  "PyMuPDF or PyPDF2 required")
    def test_lib_pdfviewer_loadFile(self):
        paneCont = sc.SizedPanel(self.frame)

        self.buttonpanel = pdfButtonPanel(paneCont, wx.ID_ANY,
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.buttonpanel.SetSizerProps(expand=True)
        self.viewer = pdfViewer(paneCont, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        self.viewer.SetSizerProps(expand=True, proportion=1)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel

        self.viewer.LoadFile(samplePdf)
        self.waitFor(500)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
