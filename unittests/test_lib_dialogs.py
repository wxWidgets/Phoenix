import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.dialogs as dialogs

#---------------------------------------------------------------------------

class lib_dialogs_Tests(wtc.WidgetTestCase):

    def test_lib_dialogsColourDialogColour(self):
        with mock.patch.object(dialogs.wx, 'ColourDialog') as dlg:
            data = wx.ColourData()
            dlg.return_value.GetColourData.return_value = data
            dlg.return_value.ShowModal.return_value = wx.ID_OK
            result = dialogs.colourDialog(self.frame, colour=wx.Colour(1, 2, 3))
        self.assertEqual(result.colour, wx.Colour(1, 2, 3).Get())

    def test_lib_dialogsColorDialogColor(self):
        with mock.patch.object(dialogs.wx, 'ColourDialog') as dlg:
            data = wx.ColourData()
            dlg.return_value.GetColourData.return_value = data
            dlg.return_value.ShowModal.return_value = wx.ID_OK
            result = dialogs.colorDialog(self.frame, color=wx.Colour(1, 2, 3))
        self.assertEqual(result.color, wx.Colour(1, 2, 3).Get())

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
