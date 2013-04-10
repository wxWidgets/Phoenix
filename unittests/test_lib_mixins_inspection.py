import imp_unittest, unittest
import wx
import wx.lib.mixins.inspection as wit

#---------------------------------------------------------------------------

class wit_TestCase(unittest.TestCase):
    
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
