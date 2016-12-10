import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class printfw_Tests(wtc.WidgetTestCase):

    def test_printfw1(self):
        # TODO: We need to figure out some way to unittest wx.PrintPreview
        # and wx.Printout...  In the meantime see samples/printing/printing.py
        pass


    def test_printfw2(self):
        wx.PREVIEW_PRINT
        wx.PREVIEW_NEXT
        wx.PREVIEW_PREVIOUS
        wx.PREVIEW_ZOOM
        wx.PREVIEW_DEFAULT

        wx.PRINTER_NO_ERROR
        wx.PRINTER_CANCELLED
        wx.PRINTER_ERROR

        wx.PREVIEW_PRINT
        wx.PREVIEW_PREVIOUS
        wx.PREVIEW_NEXT
        wx.PREVIEW_ZOOM
        wx.PREVIEW_FIRST
        wx.PREVIEW_LAST
        wx.PREVIEW_GOTO
        wx.PREVIEW_DEFAULT

        wx.ID_PREVIEW_CLOSE
        wx.ID_PREVIEW_NEXT
        wx.ID_PREVIEW_PREVIOUS
        wx.ID_PREVIEW_PRINT
        wx.ID_PREVIEW_ZOOM
        wx.ID_PREVIEW_FIRST
        wx.ID_PREVIEW_LAST
        wx.ID_PREVIEW_GOTO
        wx.ID_PREVIEW_ZOOM_IN
        wx.ID_PREVIEW_ZOOM_OUT


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
