import imp_unittest, unittest
import wtc
import wx


#---------------------------------------------------------------------------

class progdlg_Tests(wtc.WidgetTestCase):

    def test_progdlg1(self):        
        max = 50
        dlg = wx.ProgressDialog("Progress dialog example",
                                "An informative message",
                                parent=self.frame,
                                maximum=max)

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            #wx.MilliSleep(250)
            self.myYield()            
            (keepGoing, skip) = dlg.Update(count)

        dlg.Destroy()
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
