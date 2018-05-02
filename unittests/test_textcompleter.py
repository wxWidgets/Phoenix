import unittest
from unittests import wtc
import wx


#---------------------------------------------------------------------------

class testcompleter_Tests(wtc.WidgetTestCase):

    def test_textcompleterClasses(self):
        wx.TextCompleter
        wx.TextCompleterSimple

    def test_textCompleter1(self):
        class MyTextCompleter(wx.TextCompleter):
            def __init__(self):
                wx.TextCompleter.__init__(self)
            def Start(self, prefix):
                return False
            def GetNext(self):
                return ''
        t = wx.TextCtrl(self.frame)
        t.AutoComplete(MyTextCompleter())


    def test_textCompleterSimple(self):
        class MyTextCompleterSimple(wx.TextCompleterSimple):
            def __init__(self):
                wx.TextCompleterSimple.__init__(self)
            def GetCompletions(self, prefix):
                res = []
                res.append("one")
                res.append("two")
                return res
        t = wx.TextCtrl(self.frame)
        t.AutoComplete(MyTextCompleterSimple())


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
