import sys
import unittest
from unittests import wtc
import wx
##import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')

#---------------------------------------------------------------------------

class PyEvents(unittest.TestCase):

    def test_PyEvent(self):
        id = wx.Window.NewControlId()
        typ = wx.NewEventType()
        evt = wx.PyEvent(id, typ)
        evt.newAttr = "hello"
        evt2 = evt.Clone()
        self.assertTrue(type(evt2) == wx.PyEvent)
        self.assertTrue(evt is not evt2)
        self.assertTrue(getattr(evt2, 'newAttr'))
        self.assertTrue(evt.newAttr == evt2.newAttr)
        self.assertTrue(evt.Id == evt2.Id)
        self.assertTrue(evt.EventType == evt2.EventType)



    def test_PyCommandEvent(self):
        id = wx.Window.NewControlId()
        typ = wx.NewEventType()
        evt = wx.PyCommandEvent(id, typ)
        evt.newAttr = "hello"
        evt2 = evt.Clone()
        self.assertTrue(type(evt2) == wx.PyCommandEvent)
        self.assertTrue(evt is not evt2)
        self.assertTrue(getattr(evt2, 'newAttr'))
        self.assertTrue(evt.newAttr == evt2.newAttr)
        self.assertTrue(evt.Id == evt2.Id)
        self.assertTrue(evt.EventType == evt2.EventType)


    def test_PyEvtCloneRefCounts(self):
        # Since we're doing some funky stuff under the covers with Clone, make
        # sure that the reference counts on everything (before and after)
        # still make sense
        evt1 = wx.PyEvent()
        rc1 = sys.getrefcount(evt1)
        evt1.attr = 'Howdy!'
        evt2 = evt1.Clone()
        rc2 = sys.getrefcount(evt2)
        rc3 = sys.getrefcount(evt1)
        self.assertTrue(rc1 == rc2 == rc3)
        self.assertTrue(evt1.attr == evt2.attr)


    def test_CppClone(self):
        # test what happens when Clone is called from C++
        if hasattr(wx, 'testCppClone'):
            evt1 = wx.PyEvent()
            evt1.attr = 'testCppClone'
            evt2 = wx.testCppClone(evt1)
            self.assertTrue(evt1.attr == evt2.attr)


    def test_CppCloneDerived(self):
        # test what happens when Clone is called from C++
        if hasattr(wx, 'testCppClone'):
            evt1 = MyPyEvent()
            evt1.attr = 'testCppClone'
            evt2 = wx.testCppClone(evt1)
            self.assertTrue(evt1.attr == evt2.attr)
            self.assertTrue(isinstance(evt2, MyPyEvent))


    @unittest.skip('not testing refcounts for now, needs checking...')
    def test_CppCloneRefCounts(self):
        # Since we're doing some funky stuff under the covers with Clone, make
        # sure that the reference counts on everything (before and after)
        # still make sense
        if hasattr(wx, 'testCppClone'):
            evt1 = wx.PyEvent()
            rc1 = sys.getrefcount(evt1)
            evt1.attr = 'Howdy!'
            evt2 = wx.testCppClone(evt1)
            rc2 = sys.getrefcount(evt2)
            rc3 = sys.getrefcount(evt1)
            self.assertTrue(rc1 == rc2 == rc3)
            self.assertTrue(evt1.attr == evt2.attr)






class MyPyEvent(wx.PyEvent):
    def __init__(self, *args, **kw):
        wx.PyEvent.__init__(self, *args, **kw)
        self.one = 1
        self.two = 2
        self.three = 3

class MyPyCommandEvent(wx.PyCommandEvent):
    def __init__(self, *args, **kw):
        wx.PyEvent.__init__(self, *args, **kw)
        self.one = 1
        self.two = 2
        self.three = 3



class SendingPyEvents(wtc.WidgetTestCase):
    def test_PyEventDerivedClone(self):
        evt1 = MyPyEvent(id=123)
        evt1.four = 4
        evt2 = evt1.Clone()

        self.assertEqual(evt2.GetId(), 123)
        self.assertEqual(evt2.one, 1)
        self.assertEqual(evt2.two, 2)
        self.assertEqual(evt2.three, 3)
        self.assertEqual(evt2.four, 4)
        self.assertTrue(isinstance(evt2, MyPyEvent))
        self.assertTrue(evt1 is not evt2)


    def test_PyCommandEventDerivedClone(self):
        evt1 = MyPyCommandEvent(id=123)
        evt1.four = 4
        evt2 = evt1.Clone()

        self.assertEqual(evt2.GetId(), 123)
        self.assertEqual(evt2.one, 1)
        self.assertEqual(evt2.two, 2)
        self.assertEqual(evt2.three, 3)
        self.assertEqual(evt2.four, 4)
        self.assertTrue(isinstance(evt2, MyPyCommandEvent))
        self.assertTrue(evt1 is not evt2)


    def test_PyEventDerivedProcessEvent(self):
        self.flag = False

        def evtHandlerFunction(evt):
            self.assertEqual(evt.GetId(), 123)
            self.assertEqual(evt.one, 1)
            self.assertEqual(evt.two, 2)
            self.assertEqual(evt.three, 3)
            self.assertEqual(evt.four, 4)
            self.assertTrue(isinstance(evt, MyPyEvent))
            self.flag = True

        testType = wx.NewEventType()
        EVT_TEST = wx.PyEventBinder(testType)
        self.frame.Bind(EVT_TEST, evtHandlerFunction)
        evt = MyPyEvent(id=123, eventType=testType)
        evt.four = 4
        self.frame.GetEventHandler().ProcessEvent(evt)
        self.assertTrue(self.flag)


    def test_PyEventDerivedPostEvent(self):
        self.flag = False

        def evtHandlerFunction(evt):
            self.assertEqual(evt.GetId(), 123)
            self.assertEqual(evt.one, 1)
            self.assertEqual(evt.two, 2)
            self.assertEqual(evt.three, 3)
            self.assertEqual(evt.four, 4)
            self.assertTrue(isinstance(evt, MyPyEvent))
            self.flag = True

        testType = wx.NewEventType()
        EVT_TEST = wx.PyEventBinder(testType)
        self.frame.Bind(EVT_TEST, evtHandlerFunction)
        evt = MyPyEvent(id=123, eventType=testType)
        evt.four = 4
        wx.PostEvent(self.frame, evt)
        del evt
        self.myYield()
        self.assertTrue(self.flag)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
