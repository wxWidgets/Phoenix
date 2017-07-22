import unittest
import wx


#---------------------------------------------------------------------------

class IdManagerTest(unittest.TestCase):

    def test_idManager(self):
        id = wx.IdManager.ReserveId(5)
        self.assertTrue(id != wx.ID_NONE)

        wx.IdManager.UnreserveId(id, 5)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
