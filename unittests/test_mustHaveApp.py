import unittest
import wx


#---------------------------------------------------------------------------

class TestMustHaveApp(unittest.TestCase):

    def test_mustHaveApp0(self):
        """Test that an exception is raised if there is no app"""
        with self.assertRaises(wx.PyNoAppError):
            frame = wx.Frame(None)
            frame.Close()


    def test_mustHaveApp1(self):
        """Create App and then create a frame"""
        app = wx.App()
        frame = wx.Frame(None)
        frame.Show()
        frame.Close()
        app.MainLoop()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
