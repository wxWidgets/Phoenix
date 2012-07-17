import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class filehistory_Tests(wtc.WidgetTestCase):

    def test_filehistory1(self):
        fh = wx.FileHistory()
        for fn in "one two three four".split():
            fh.AddFileToHistory(fn)
            
        self.assertEqual(fh.GetCount(), 4)
        self.assertEqual(fh.Count, 4)
        self.assertEqual(fh.GetHistoryFile(1), 'three')  # they are in LIFO order
        m = wx.Menu()
        fh.AddFilesToMenu(m)
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
