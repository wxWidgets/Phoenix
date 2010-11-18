import unittest2
import wx


#---------------------------------------------------------------------------

class MouseState(unittest2.TestCase):
    
    def test_MouseState(self):
        ms = wx.MouseState()
        ms.controlDown
        ms.shiftDown
        ms.altDown
        ms.cmdDown
        
        ms.x
        ms.y
        ms.leftIsDown
        ms.middleIsDown
        ms.rightIsDown
        ms.aux1IsDown
        ms.aux2IsDown
        ms.Position
        
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
