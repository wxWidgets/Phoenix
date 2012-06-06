import imp_unittest, unittest
import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class joystick_Tests(wtc.WidgetTestCase):

    def test_joystick1(self):
        wx.JOYSTICK1
        wx.JOYSTICK2
        wx.JOY_BUTTON_ANY
        wx.JOY_BUTTON1
        wx.JOY_BUTTON2
        wx.JOY_BUTTON3
        wx.JOY_BUTTON4
        
        wx.wxEVT_JOY_BUTTON_DOWN
        wx.wxEVT_JOY_BUTTON_UP
        wx.wxEVT_JOY_MOVE
        wx.wxEVT_JOY_ZMOVE

        wx.EVT_JOY_BUTTON_DOWN
        wx.EVT_JOY_BUTTON_UP
        wx.EVT_JOY_MOVE
        wx.EVT_JOY_ZMOVE
        wx.EVT_JOYSTICK_EVENTS

    
    def test_joystick2(self):
        # Creating a Joystick object should fail on Mac.
        if 'wxMac' in wx.PlatformInfo:
            with self.assertRaises(NotImplementedError):
                j = wx.adv.Joystick()
        else:
            j = wx.adv.Joystick()  
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
