import imp_unittest, unittest
import wtc
import wx
import os

import wx.lib.sized_controls as sc
try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    havePyPDF = True
except ImportError:
    havePyPDF = False  # Assume an import error is due to missing pyPdf

dataDir = os.path.join(os.path.dirname(__file__), "data")
samplePdf = os.path.join(dataDir, "sample.pdf")

#---------------------------------------------------------------------------

@unittest.skip('crashing on OSX...')  # problem with a nested yield in GenericProgressDialog?
class lib_pdfviewer_pdfviewer_Tests(wtc.WidgetTestCase):
        
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_pdfviewerButtonPanelCtor(self):
        bp = pdfButtonPanel(self.frame, wx.NewId(),
                            wx.DefaultPosition, wx.DefaultSize, 0)

    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_pdfviewerPdfViewerCtor(self):
        pv = pdfViewer(self.frame, wx.NewId(), wx.DefaultPosition,
                       wx.DefaultSize,
                       wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)

    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_loadFile(self):
        paneCont = sc.SizedPanel(self.frame)

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
        
        self.viewer.LoadFile(samplePdf)
        self.waitFor(500)
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
