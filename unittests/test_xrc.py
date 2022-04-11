import unittest
from unittests import wtc
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
        self.assertTrue(ctrl is not None)
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
        xmlres.LoadFromBuffer(data)
        self.checkXmlRes(xmlres)

    def test_xrc4(self):
        xmlres = xrc.XmlResource(xrcFile)
        p = xmlres.LoadObjectRecursively(self.frame, 'MainPanel', 'wxPanel')
        self.assertNotEqual(p, None)
        self.frame.SendSizeEvent()
        self.myYield()

    #---------------------------------------------------------------------------
    # Tests for custom handlers

    # This test does not allow for 2-phase create or creating the instance of
    # the resource before filling it with widgets or etc. See also the next
    # test and try to keep the two of them in sync as much as possible.
    def test_xrc5(self):
        resource = b'''<?xml version="1.0"?>
            <resource>
            <object class="wxFrame" name="MainFrame">
                <size>400,250</size>
                <title>This is a test</title>
                <!-- Notice that the class is NOT a standard wx class -->
                <object class="MyCustomPanel" name="MyPanel">
                    <size>200,100</size>
                    <object class="wxStaticText" name="label1">
                        <label>This panel is a custom class derived from wx.Panel,\nand is loaded by a custom XmlResourceHandler.</label>
                        <pos>10,10</pos>
                    </object>
                </object>
            </object>
            </resource>'''

        # this is the class that will be created for the resource
        class MyCustomPanel(wx.Panel):
            def __init__(self, parent, id, pos, size, style, name):
                wx.Panel.__init__(self, parent, id, pos, size, style, name)

                # This is the little bit of customization that we do for this
                # silly example.
                self.Bind(wx.EVT_SIZE, self.OnSize)
                t = wx.StaticText(self, -1, "MyCustomPanel")
                f = t.GetFont()
                f.SetWeight(wx.BOLD)
                f.SetPointSize(f.GetPointSize()+2)
                t.SetFont(f)
                self.t = t

            def OnSize(self, evt):
                sz = self.GetSize()
                w, h = self.t.GetTextExtent(self.t.GetLabel())
                self.t.SetPosition(((sz.width-w)//2, (sz.height-h)//2))


        # this is the handler class that will create the resource item
        class MyCustomPanelXmlHandler(xrc.XmlResourceHandler):
            def __init__(self):
                xrc.XmlResourceHandler.__init__(self)
                # Specify the styles recognized by objects of this type
                self.AddStyle("wxTAB_TRAVERSAL", wx.TAB_TRAVERSAL)
                self.AddStyle("wxWS_EX_VALIDATE_RECURSIVELY", wx.WS_EX_VALIDATE_RECURSIVELY)
                self.AddStyle("wxCLIP_CHILDREN", wx.CLIP_CHILDREN)
                self.AddWindowStyles()

            def CanHandle(self, node):
                return self.IsOfClass(node, "MyCustomPanel")

            def DoCreateResource(self):
                # Ensure that the instance hasn't been created yet (since
                # we're not using 2-phase create)
                assert self.GetInstance() is None

                # Now create the object
                panel = MyCustomPanel(self.GetParentAsWindow(),
                                      self.GetID(),
                                      self.GetPosition(),
                                      self.GetSize(),
                                      self.GetStyle("style", wx.TAB_TRAVERSAL),
                                      self.GetName()
                                      )
                self.SetupWindow(panel)
                self.CreateChildren(panel)
                return panel

        # now load it
        xmlres = xrc.XmlResource()
        xmlres.InsertHandler( MyCustomPanelXmlHandler() )
        success = xmlres.LoadFromBuffer(resource)

        f = xmlres.LoadFrame(self.frame, 'MainFrame')
        self.assertNotEqual(f, None)
        f.Show()
        self.myYield()

        panel = xrc.XRCCTRL(f, 'MyPanel')
        self.assertNotEqual(panel, None)
        self.assertTrue(isinstance(panel, MyCustomPanel))



    # This test shows how to do basically the same as above while still
    # allowing the instance to be created before loading the content.

    def test_xrc6(self):
        resource = b'''<?xml version="1.0"?>
            <resource>
            <object class="wxFrame" name="MainFrame">
                <size>400,250</size>
                <title>This is a test</title>
                <!-- Notice that the class is NOT a standard wx class -->
                <object class="MyCustomPanel" name="MyPanel">
                    <size>200,100</size>
                    <object class="wxStaticText" name="label1">
                        <label>This panel is a custom class derived from wx.Panel,\nand is loaded by a custom XmlResourceHandler.</label>
                        <pos>10,10</pos>
                    </object>
                </object>
            </object>
            </resource>'''

        # this is the class that will be created for the resource
        class MyCustomPanel(wx.Panel):
            def __init__(self):
                wx.Panel.__init__(self)  # create only the instance, not the widget

            def Create(self, parent, id, pos, size, style, name):
                wx.Panel.Create(self, parent, id, pos, size, style, name)
                self.Bind(wx.EVT_SIZE, self.OnSize)
                t = wx.StaticText(self, -1, "MyCustomPanel")
                f = t.GetFont()
                f.SetWeight(wx.BOLD)
                f.SetPointSize(f.GetPointSize()+2)
                t.SetFont(f)
                self.t = t

            def OnSize(self, evt):
                sz = self.GetSize()
                w, h = self.t.GetTextExtent(self.t.GetLabel())
                self.t.SetPosition(((sz.width-w)//2, (sz.height-h)//2))


        # this is the handler class that will create the resource item
        class MyCustomPanelXmlHandler(xrc.XmlResourceHandler):
            def __init__(self):
                xrc.XmlResourceHandler.__init__(self)
                # Specify the styles recognized by objects of this type
                self.AddStyle("wxTAB_TRAVERSAL", wx.TAB_TRAVERSAL)
                self.AddStyle("wxWS_EX_VALIDATE_RECURSIVELY", wx.WS_EX_VALIDATE_RECURSIVELY)
                self.AddStyle("wxCLIP_CHILDREN", wx.CLIP_CHILDREN)
                self.AddWindowStyles()

            def CanHandle(self, node):
                return self.IsOfClass(node, "MyCustomPanel")

            def DoCreateResource(self):
                panel = self.GetInstance()
                if panel is None:
                    # if not, then create the instance (but not the window)
                    panel = MyCustomPanel()

                # Now create the UI object
                panel.Create(self.GetParentAsWindow(),
                             self.GetID(),
                             self.GetPosition(),
                             self.GetSize(),
                             self.GetStyle("style", wx.TAB_TRAVERSAL),
                             self.GetName()
                             )
                self.SetupWindow(panel)
                self.CreateChildren(panel)
                return panel

        # now load it
        xmlres = xrc.XmlResource()
        xmlres.InsertHandler( MyCustomPanelXmlHandler() )
        success = xmlres.LoadFromBuffer(resource)

        f = xmlres.LoadFrame(self.frame, 'MainFrame')
        self.assertNotEqual(f, None)
        f.Show()
        self.myYield()

        panel = xrc.XRCCTRL(f, 'MyPanel')
        self.assertNotEqual(panel, None)
        self.assertTrue(isinstance(panel, MyCustomPanel))



    #---------------------------------------------------------------------------
    # Tests for the Subclass Factory
    def test_xrc7(self):
        resource = b'''<?xml version="1.0"?>
            <resource>
                <!-- Notice that the class IS a standard wx class and that a subclass is specified -->
                <object class="wxPanel" name="MyPanel" subclass="unittests.xrcfactorytest.MyCustomPanel">
                    <size>200,100</size>
                    <object class="wxStaticText" name="label1">
                        <label>This panel is a custom class derived from wx.Panel,\nand is loaded by the Python SubclassFactory.</label>
                        <pos>10,10</pos>
                    </object>
                </object>
            </resource>'''


        # now load it
        xmlres = xrc.XmlResource()
        success = xmlres.LoadFromBuffer(resource)

        panel = xmlres.LoadPanel(self.frame, "MyPanel")
        self.frame.SendSizeEvent()
        self.myYield()

        self.assertNotEqual(panel, None)
        from unittests import xrcfactorytest
        self.assertTrue(isinstance(panel, xrcfactorytest.MyCustomPanel))



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
