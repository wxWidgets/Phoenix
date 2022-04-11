import unittest
from unittests import wtc
import wx
import os

THIS_FILE = os.path.abspath(__file__)

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

    def test_dirctrlGetPath(self):
        d = wx.GenericDirCtrl(self.frame)
        d.ExpandPath(os.path.dirname(THIS_FILE))
        d.SelectPath(THIS_FILE)
        p = d.GetPath()
        assert isinstance(p, str)
        assert p == THIS_FILE

    def test_dirctrlGetPaths(self):
        d = wx.GenericDirCtrl(self.frame, style=wx.DIRCTRL_MULTIPLE)
        d.ExpandPath(os.path.dirname(THIS_FILE))
        d.SelectPaths([THIS_FILE])
        p = d.GetPaths()
        assert isinstance(p, list)
        assert p == [THIS_FILE]



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
