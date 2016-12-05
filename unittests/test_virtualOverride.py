import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

# This test will ensure that a virtual C++ method from a base class can
# be overridden in a derived class implemented in Python, and that when
# the C++ method is called from C++ that the Python override is called.
# In addition the Python override will pass the call on to the base class
# implementation and this test will ensure that is successful as well.
#
# The AddChild method is a good cantidate for this test because it is
# easy to induce a call from C++ (just create a child window) and it is
# easy to test if the calling the base class AddChild works (the length
# of the GetChildren list will increase.)

class MyTestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)
        self.methodCalled = False

    def AddChild(self, child):
        self.methodCalled = True
        if 1:
            super(MyTestPanel, self).AddChild(child)
        else:
            wx.Panel.AddChild(self, child)


class virtualOverride_Tests(wtc.WidgetTestCase):

    def test_virtualOverride(self):
        p = MyTestPanel(self.frame)
        count = len(p.Children)
        b = wx.Button(p, -1, "Hello, I am a button")
        self.assertTrue(p.methodCalled)
        self.assertTrue(len(p.Children) == count+1)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
