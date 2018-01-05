import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class dtor_Tests(wtc.WidgetTestCase):

    def test_dtor(self):
        # Test that a __dtor__ method is called when a wrapped C++ class is
        # destroyed

        class MyPanel(wx.Panel):
            def __init__(self, parent):
                super(MyPanel, self).__init__(parent)
                self.Parent.dtor_called = False

            def __dtor__(self):
                self.Parent.dtor_called = True


        panel = MyPanel(self.frame)
        self.myYield()
        assert not self.frame.dtor_called
        panel.Destroy()
        self.myYield()
        assert self.frame.dtor_called

