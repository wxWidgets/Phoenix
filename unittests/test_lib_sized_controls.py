import unittest
from unittests import wtc
import wx
import os

import wx.lib.sized_controls as sc

#---------------------------------------------------------------------------

class sizedFrame_Tests(wtc.WidgetTestCase):

    def test_frameStyles(self):
        wx.FRAME_NO_TASKBAR
        wx.FRAME_TOOL_WINDOW
        wx.FRAME_FLOAT_ON_PARENT
        wx.FRAME_SHAPED


    def test_frameCtors(self):
        f = sc.SizedFrame(None)
        f.Show()
        f.Close()
        f = sc.SizedFrame(self.frame, title="Title", pos=(50,50), size=(100,100))
        f.Show()
        f.Close()
        #f = sc.SizedFrame()
        #f.Create(None, title='2 phase')
        #f.Show()
        #f.Close()

    #def test_frameTopLevelTweaks(self):
    #    # test a couple tweaks added in wx.TopLevelWidnow
    #    f = sc.SizedFrame()
    #    f.MacSetMetalAppearance(True)
    #    f.Create(None)
    #    f.Show()
    #    f.MacGetTopLevelWindowRef()
    #    f.Close()


    def test_frameProperties(self):
        f = sc.SizedFrame(None)
        f.Show()

        f.DefaultItem
        f.Icon
        f.Title
        f.TmpDefaultItem
        f.OSXModified
        f.MacMetalAppearance

        f.Close()


#---------------------------------------------------------------------------


class sizedDialog_Tests(wtc.WidgetTestCase):

    def runDialog(self, dlg):
        # Add some buttons
        ok = wx.Button(dlg.GetContentsPane(), wx.ID_OK, pos=(10,10))
        cancel = wx.Button(dlg.GetContentsPane(), wx.ID_CANCEL, pos=(100,10))

        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        val = dlg.ShowModal()
        dlg.Destroy()
        self.assertTrue(val == wx.ID_OK)
        self.myYield()


    #def test_dialogDefaultCtor(self):
    #    dlg = sc.SizedDialog()
    #    dlg.Create(None, title='dialog')
    #    self.runDialog(dlg)

    def test_dialog1(self):
        # with parent
        dlg = sc.SizedDialog(self.frame, title='Hello')
        self.runDialog(dlg)

    def test_dialog2(self):
        # without parent
        dlg = sc.SizedDialog(None, title='World')
        self.runDialog(dlg)

    def test_dialogTextSizer(self):
        dlg = sc.SizedDialog(self.frame, title='Hello')
        s = dlg.CreateTextSizer("This is a test.\nThis is only a test.\nHello World")
        self.assertTrue(isinstance(s, wx.Sizer))
        self.assertTrue(len(s.Children) == 3)
        self.runDialog(dlg)


#---------------------------------------------------------------------------


class sizedPanel_Tests(wtc.WidgetTestCase):

    def test_panelCtor(self):
        p = sc.SizedPanel(self.frame)

    #def test_panelDefaultCtor(self):
    #    p = sc.SizedPanel()
    #    p.Create(self.frame)


#---------------------------------------------------------------------------


class sizedScrolledPanel_Tests(wtc.WidgetTestCase):

    def test_panelCtor(self):
        p = sc.SizedScrolledPanel(self.frame)

    #def test_panelDefaultCtor(self):
    #    p = sc.SizedScrolledPanel()
    #    p.Create(self.frame)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
