import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class preferences_Tests(wtc.WidgetTestCase):

    def test_preferences1(self):

        class MyPrefsPanel(wx.Panel):
            def __init__(self, parent):
                wx.Panel.__init__(self, parent)
                cb1 = wx.CheckBox(self, -1, "Option 1")
                cb2 = wx.CheckBox(self, -1, "Option 2")
                box = wx.BoxSizer(wx.VERTICAL)
                box.Add(cb1, 0, wx.ALL, 5)
                box.Add(cb2, 0, wx.ALL, 5)
                self.Sizer = wx.BoxSizer()
                self.Sizer.Add(box, 0, wx.ALL, 10)

        class MyPrefsPage(wx.PreferencesPage):
            def GetName(self):
                return 'MyPrefsPage'
            def GetIcon(self):
                return wx.ArtProvider.GetBitmapBundle(wx.ART_HELP, wx.ART_TOOLBAR)
            def CreateWindow(self, parent):
                return MyPrefsPanel(parent)

        prefEd = wx.PreferencesEditor()
        page1 = MyPrefsPage()
        page2 = MyPrefsPage()
        prefEd.AddPage(page1)
        prefEd.AddPage(page2)
        wx.CallLater(250, prefEd.Dismiss)
        prefEd.Show(self.frame)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
