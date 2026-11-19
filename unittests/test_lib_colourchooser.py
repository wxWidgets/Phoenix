import sys
import unittest
from unittest import mock
from unittests import wtc
import wx

from wx.lib.colourchooser.canvas import Canvas

from wx.lib.colourchooser.pycolourchooser import PyColourChooser

#---------------------------------------------------------------------------

class lib_colourchooser_Tests(wtc.WidgetTestCase):

    def test_lib_colourchooserCustomColourClick(self):
        chooser = PyColourChooser(self.frame, -1)
        chooser.onCustomClick(None, chooser.custom_boxs[0])

    def test_lib_colourchooserCanvasZeroSize(self):
        # The size event handler makes a new buffer the canvas's size
        with mock.patch.object(sys, 'excepthook') as excepthook:
            canvas = Canvas(self.frame, -1)
            canvas.SetSize(0, 0)
            self.myYield()
            canvas.ReDraw()
        self.assertFalse(excepthook.called)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
