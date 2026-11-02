import unittest

from wx.tools.dbg import Logger

#---------------------------------------------------------------------------

class tools_dbg_Tests(unittest.TestCase):

    def test_tools_dbgState(self):
        dbg = Logger('test_tools_dbg')
        self.assertFalse(dbg.IsEnabled())
        self.assertFalse(dbg.IsSuspended())

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
