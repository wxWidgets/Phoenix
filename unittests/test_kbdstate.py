import unittest2
import wxPhoenix as wx


#---------------------------------------------------------------------------

class KeyboardState(unittest2.TestCase):
    
    def test_KeyboardState(self):
        ks = wx.KeyboardState(False, True, False, True)
        ks.controlDown
        ks.shiftDown
        ks.altDown
        ks.cmdDown
        
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
