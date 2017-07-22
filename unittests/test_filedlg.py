import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class filedlg_Tests(wtc.WidgetTestCase):

    def test_filedlgFlags(self):
        wx.FD_OPEN
        wx.FD_SAVE
        wx.FD_OVERWRITE_PROMPT
        wx.FD_FILE_MUST_EXIST
        wx.FD_MULTIPLE
        wx.FD_CHANGE_DIR
        wx.FD_PREVIEW

    def test_filedlg(self):
        # a typical use case
        dlg = wx.FileDialog(self.frame, 'message', os.getcwd(), "",
                            wildcard="Python source (*.py)|*.py")
        dlg.Destroy()

    def test_filedlgProperties(self):
        dlg = wx.FileDialog(None)
        dlg.Directory
        dlg.ExtraControl
        dlg.Filename
        dlg.FilterIndex
        dlg.Message
        dlg.Path
        dlg.Wildcard
        dlg.Filenames
        dlg.Paths
        dlg.Destroy()

    def test_filedlgTweaks(self):
        dlg = wx.FileDialog(None, style=wx.FD_MULTIPLE)
        f = dlg.GetFilenames()
        p = dlg.GetPaths()
        self.assertTrue(isinstance(f, list))
        self.assertTrue(isinstance(p, list))
        dlg.Destroy()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
