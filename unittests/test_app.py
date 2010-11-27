import unittest2
import wxPhoenix as wx


#---------------------------------------------------------------------------

class App(unittest2.TestCase):
    
    def test_App(self):
        app = wx.App()
    
    def test_App_OnInit(self):
            
        class MyApp(wx.App):
            def OnInit(self):
                self.onInit_called = True
                return True
                
        app = MyApp()
        self.assertTrue(app.onInit_called)
            
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
