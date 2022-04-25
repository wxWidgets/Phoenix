import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class filectrl_Tests(wtc.WidgetTestCase):

    def test_filectrl1(self):
        fc = wx.FileCtrl(self.frame)

    def test_filectrl2(self):
        fc = wx.FileCtrl()
        fc.Create(self.frame)

    def test_filectrl3(self):
        wx.FC_OPEN
        wx.FC_SAVE
        wx.FC_MULTIPLE
        wx.FC_NOSHOWHIDDEN
        wx.FC_DEFAULT_STYLE

        wx.wxEVT_FILECTRL_SELECTIONCHANGED
        wx.wxEVT_FILECTRL_FILEACTIVATED
        wx.wxEVT_FILECTRL_FOLDERCHANGED
        wx.wxEVT_FILECTRL_FILTERCHANGED
        wx.EVT_FILECTRL_SELECTIONCHANGED
        wx.EVT_FILECTRL_FILEACTIVATED
        wx.EVT_FILECTRL_FOLDERCHANGED
        wx.EVT_FILECTRL_FILTERCHANGED
        wx.FileCtrlEvent


    def test_filectrl4(self):
        fc = wx.FileCtrl(self.frame,
                         defaultDirectory=os.path.dirname(__file__),
                         defaultFilename=os.path.basename(__file__),
                         style=wx.FC_OPEN)
        self.waitFor(300)

        self.assertEqual(fc.GetFilename(), os.path.basename(__file__))
        self.assertEqual(fc.GetPath(), os.path.abspath(__file__))
        self.assertEqual(fc.Filename, os.path.basename(__file__))
        self.assertEqual(fc.Path, os.path.abspath(__file__))


    def test_filectrl5(self):
        fc = wx.FileCtrl(self.frame,
                         defaultDirectory=os.path.dirname(__file__),
                         defaultFilename=os.path.basename(__file__),
                         style=wx.FC_OPEN|wx.FC_MULTIPLE)
        self.waitFor(300)

        self.assertEqual(fc.GetFilenames(), [os.path.basename(__file__)])
        self.assertEqual(fc.GetPaths(), [os.path.abspath(__file__)])
        self.assertEqual(fc.Filenames, [os.path.basename(__file__)])
        self.assertEqual(fc.Paths, [os.path.abspath(__file__)])


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
