import unittest
import wx


#---------------------------------------------------------------------------

class KeyboardState(unittest.TestCase):

    def test_KeyboardState(self):
        ks = wx.KeyboardState(False, True, False, True)
        ks.controlDown
        ks.shiftDown
        ks.altDown
        ks.cmdDown



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
