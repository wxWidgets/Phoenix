import unittest
from unittests import wtc
import wx


#---------------------------------------------------------------------------

class combo_Tests(wtc.WidgetTestCase):

    def test_comboConstants(self):
        wx.CC_SPECIAL_DCLICK
        wx.CC_STD_BUTTON

        wx.ComboCtrlFeatures
        wx.ComboCtrlFeatures.MovableButton
        wx.ComboCtrlFeatures.BitmapButton
        wx.ComboCtrlFeatures.ButtonSpacing
        wx.ComboCtrlFeatures.TextIndent
        wx.ComboCtrlFeatures.PaintControl
        wx.ComboCtrlFeatures.PaintWritable
        wx.ComboCtrlFeatures.Borderless
        wx.ComboCtrlFeatures.All


    def test_combo1(self):
        ns = self.execSample('combo/combo1.py')
        frame = ns.TestFrame(self.frame)
        frame.Show()
        frame.cc.SetValueByUser('Item-25')
        self.waitFor(100)
        frame.cc.Popup()
        self.waitFor(100)
        frame.Close()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
