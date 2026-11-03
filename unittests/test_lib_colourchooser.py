import unittest
from unittests import wtc
import wx

from wx.lib.colourchooser.pycolourchooser import PyColourChooser

#---------------------------------------------------------------------------

class lib_colourchooser_Tests(wtc.WidgetTestCase):

    def test_lib_colourchooserCustomColourClick(self):
        chooser = PyColourChooser(self.frame, -1)
        chooser.onCustomClick(None, chooser.custom_boxs[0])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
