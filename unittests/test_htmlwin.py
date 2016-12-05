import unittest
from unittests import wtc
import wx
import wx.html

import os
helpPath = os.path.join(os.path.dirname(__file__), 'helpfiles')

#---------------------------------------------------------------------------

class htmlwin_Tests(wtc.WidgetTestCase):

    def test_htmlwin1(self):
        obj = wx.html.HtmlWindow(self.frame)

    def test_htmlwin2(self):
        obj = wx.html.HtmlWindow()
        obj.Create(self.frame)

    def test_htmlwin3(self):
        obj = wx.html.HtmlWindow(self.frame)
        obj.LoadFile(os.path.join(helpPath, 'main.htm'))
        self.frame.SendSizeEvent()
        self.myYield()


    def test_htmlwin4(self):
        noLog = wx.LogNull()
        obj = wx.html.HtmlWindow(self.frame)
        obj.LoadPage('http://www.google.com/')
        self.frame.SendSizeEvent()
        self.myYield()


    def test_htmlwin5(self):
        obj = wx.html.HtmlWindow(self.frame)
        obj.SetPage("<html><body>Hello, world!</body></html>")
        self.frame.SendSizeEvent()
        self.myYield()

    def test_htmlwin6(self):
        obj = wx.html.HtmlWindow(self.frame)
        self.frame.SendSizeEvent()
        self.myYield()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
