import unittest2
import wxPhoenix as wx

#---------------------------------------------------------------------------

class MouseState(unittest2.TestCase):
    
    def test_MouseState(self):
        ms = wx.MouseState()

        # Just check that the properties exist, the getters will also be called in the process
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
