import unittest
from unittests import wtc
import wx


#---------------------------------------------------------------------------

class MyEventFilter(wx.EventFilter):
    def __init__(self):
        wx.EventFilter.__init__(self)
        wx.EvtHandler.AddFilter(self)
        self.flag = False

    def __del__(self):
        wx.EvtHandler.RemoveFilter(self)

    def FilterEvent(self, event):
        t = event.GetEventType()
        if t == wx.EVT_HELP.typeId:
            self.flag = True
        return self.Event_Skip

class eventfilter_Tests(wtc.WidgetTestCase):
    def test_EventFilter_ctor(self):
        with self.assertRaises(TypeError):
            # it's an abstract class, so it can't be instantiated
            evt = wx.EventFilter()

    def test_EventFilter_subclass(self):
        filter = MyEventFilter()
        wx.PostEvent(self.frame, wx.PyCommandEvent(wx.EVT_HELP.typeId))
        self.myYield()
        self.assertTrue(filter.flag)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
