import imp_unittest, unittest
import wtc
import wx
import wx.xrc as xrc
import os

xrcFile = os.path.join(os.path.dirname(__file__), 'xrctest.xrc')

#---------------------------------------------------------------------------

class xrc_Tests(wtc.WidgetTestCase):
    
    def checkXmlRes(self, xmlres):
        assert isinstance(xmlres, xrc.XmlResource)
        f = xmlres.LoadFrame(self.frame, 'MainFrame')
        self.assertNotEqual(f, None) 
        f.Show()

        self.myYield()
        
        id = xrc.XRCID('MainPanel')
        self.assertTrue(id != -1)
        self.assertTrue(isinstance(id, int))
        
        ctrl = xrc.XRCCTRL(f, 'TitleText')
        self.assertTrue(ctrl != None)
        self.assertTrue(isinstance(ctrl, wx.StaticText))
        
        
        

    def test_xrc1(self):
        xmlres = xrc.XmlResource(xrcFile)
        self.checkXmlRes(xmlres)

    def test_xrc2(self):
        xmlres = xrc.XmlResource()
        xmlres.LoadFile(xrcFile)
        self.checkXmlRes(xmlres)

    def test_xrc3(self):
        xmlres = xrc.XmlResource()
        with open(xrcFile, 'rb') as f:
            data = f.read()
        xmlres.LoadFromString(data)
        self.checkXmlRes(xmlres)

    def test_xrc4(self):
        xmlres = xrc.XmlResource(xrcFile)
        p = xmlres.LoadObjectRecursively(self.frame, 'MainPanel', 'wxPanel')
        self.assertNotEqual(p, None) 
        self.frame.SendSizeEvent()
        self.myYield()
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
