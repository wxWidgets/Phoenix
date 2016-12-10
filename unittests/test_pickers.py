import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class pickers_Tests(wtc.WidgetTestCase):

    def test_pickersColour(self):
        p = wx.ColourPickerCtrl(self.frame, colour='blue')
        self.assertTrue(p.GetColour() == wx.Colour(0, 0, 0xff))

    def test_pickersColourConstants(self):
        wx.CLRP_USE_TEXTCTRL
        wx.CLRP_DEFAULT_STYLE
        wx.CLRP_SHOW_LABEL
        wx.wxEVT_COMMAND_COLOURPICKER_CHANGED
        wx.EVT_COLOURPICKER_CHANGED
        wx.ColourPickerEvent


    def test_pickersFile(self):
        p = wx.FilePickerCtrl(self.frame, path='/tmp', wildcard='*.foo')
        self.assertTrue(p.Path == '/tmp')

    def test_pickersFileConstants(self):
        wx.FLP_OPEN
        wx.FLP_SAVE
        wx.FLP_OVERWRITE_PROMPT
        wx.FLP_FILE_MUST_EXIST
        wx.FLP_CHANGE_DIR
        wx.FLP_SMALL
        wx.FLP_USE_TEXTCTRL
        wx.FLP_DEFAULT_STYLE

        wx.DIRP_DIR_MUST_EXIST
        wx.DIRP_CHANGE_DIR
        wx.DIRP_SMALL
        wx.DIRP_USE_TEXTCTRL
        wx.DIRP_DEFAULT_STYLE

        wx.wxEVT_COMMAND_FILEPICKER_CHANGED
        wx.wxEVT_COMMAND_DIRPICKER_CHANGED
        wx.EVT_FILEPICKER_CHANGED
        wx.EVT_DIRPICKER_CHANGED
        wx.FileDirPickerEvent


    def test_pickersDir(self):
        p = wx.DirPickerCtrl(self.frame, path='/tmp')
        self.assertTrue(p.Path == '/tmp')

    def test_pickersFont(self):
        p = wx.FontPickerCtrl(self.frame, font=wx.NORMAL_FONT)

    def test_pickersFontConstatnt(self):
        wx.FNTP_FONTDESC_AS_LABEL
        wx.FNTP_USEFONT_FOR_LABEL
        wx.FONTBTN_DEFAULT_STYLE
        wx.FNTP_USE_TEXTCTRL
        wx.FNTP_DEFAULT_STYLE
        wx.wxEVT_COMMAND_FONTPICKER_CHANGED;
        wx.EVT_FONTPICKER_CHANGED
        wx.FontPickerEvent


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
