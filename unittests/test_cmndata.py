import unittest
from unittests import wtc
import wx
import six

#---------------------------------------------------------------------------

class cmndata_tests(wtc.WidgetTestCase):

    def test_cmndataClassConstructors(self):
        psdd1 = wx.PageSetupDialogData()
        pd1 = wx.PrintData()
        pdd1 = wx.PrintDialogData()

        psdd2 = wx.PageSetupDialogData(pd1)
        psdd3 = wx.PageSetupDialogData(psdd2)

        pd2 = wx.PrintData(pd1)

        pdd2 = wx.PrintDialogData(pdd1)
        pdd3 = wx.PrintDialogData(pd1)



    def test_cppMethods(self):
        pd = wx.PrintData()
        data = pd.GetPrivData()
        pd.SetPrivData(data)

        # property for the same methods
        data = pd.PrivData
        pd.PrivData = data


    def test_nonzero(self):
        psdd = wx.PageSetupDialogData()
        pd = wx.PrintData()
        pdd = wx.PrintDialogData()

        if six.PY3:
            psdd.__bool__()
            pd.__bool__()
            pdd.__bool__()
        else:
            psdd.__nonzero__()
            pd.__nonzero__()
            pdd.__nonzero__()


    def test_PD_PaperSize(self):
        pd = wx.PrintData()
        pd.GetPaperSize()
        pd.SetPaperSize( wx.Size(int(8.5*300), 11*300) )
        pd.PaperSize


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
