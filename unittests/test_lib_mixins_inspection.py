import unittest
import time
import wx
import wx.lib.mixins.inspection as wit

#---------------------------------------------------------------------------

class wit_TestCase(unittest.TestCase):

    def tearDown(self):
        '''
        OnClose can trigger:
            AttributeError: 'Crust' object has no attribute 'lastsashpos'
         so we'll ensure that the InspectionFrame's crust has that attr.
        '''
        windows = wx.GetTopLevelWindows()
        for window in windows:
            if type(window) == wx.lib.inspection.InspectionFrame:
                if hasattr(window, 'crust'):
                    pass
                    if not hasattr(window.crust, 'lastsashpos'):
                        window.crust.lastsashpos = -1

        # class _InspectionHighlighter's FlickerTLW method invokes
        # wx.CallLater(300, self._Toggle, tlw),
        # so let's give it a chance to run:
        time.sleep(0.3)
        super(wit_TestCase, self).tearDown()

    def test_App(self):
        app = wit.InspectableApp()

    def test_App_OnInit(self):
        class MyApp(wit.InspectableApp):
            def OnInit(self):
                self.onInit_called = True
                self.ShowInspectionTool()
                return True
        app = MyApp()
        self.assertTrue(app.onInit_called)

    def test_Wit_Mixin(self):
        class MyApp(wx.App, wit.InspectionMixin):
            def OnInit(self):
                self.onInit_called = True
                self.Init()
                self.ShowInspectionTool()
                return True
        app = MyApp()
        self.assertTrue(app.onInit_called)




#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
