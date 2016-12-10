import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class dirctrl_Tests(wtc.WidgetTestCase):

    def test_dirctrlCtor(self):
        d = wx.GenericDirCtrl(self.frame)


    def test_dirctrlDefaultCtor(self):
        d = wx.GenericDirCtrl()
        d.Create(self.frame)


    def test_dirctrlFlags(self):
        wx.DIRCTRL_DIR_ONLY
        wx.DIRCTRL_SELECT_FIRST
        wx.DIRCTRL_3D_INTERNAL
        wx.DIRCTRL_EDIT_LABELS
        wx.DIRCTRL_MULTIPLE

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
