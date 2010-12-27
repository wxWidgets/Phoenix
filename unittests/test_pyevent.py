import sys
import unittest2
import wxPhoenix as wx
##import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')

from wxPhoenix import siplib

#---------------------------------------------------------------------------

class PyEvents(unittest2.TestCase):
    
    def test_PyEvent(self):                    
        id = wx.NewId()
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
        id = wx.NewId()
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
        #print '\n****', rc1, rc2, rc3
        self.assertTrue(rc1 == rc2 == rc3)
        self.assertTrue(evt1.attr == evt2.attr)
        

    def test_CppClone(self):
        # test what happens when Clone is called from C++
        if hasattr(wx, 'testCppClone'):
            evt1 = wx.PyEvent()
            evt1.attr = 'testCppClone'
            evt2 = wx.testCppClone(evt1)
            self.assertTrue(evt1.attr == evt2.attr)
         
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
            #print '\n****', rc1, rc2, rc3
            ##self.assertTrue(rc1 == rc2 == rc3)  TODO: rc2 has an extra refcount.  Why?
            self.assertTrue(evt1.attr == evt2.attr)

    #def test_AA(self):
        #class MyEvent(wx.PyEvent):
            #def __init__(self, name):
                #wx.PyEvent.__init__(self)
                #self.name = name                
            #def __del__(self):
                #print '\n-=-=-= __del__:', self.name
                
        #evt1 = MyEvent('orig')
        #evt2 = evt1.Clone()
        #evt2.name += ' clone'
        #evt3 = wx.testCppClone(evt1)
        #evt3.name += ' clone2'
        #print sys.getrefcount(evt1), sys.getrefcount(evt2), sys.getrefcount(evt3)
        #print siplib.ispyowned(evt1), siplib.ispyowned(evt2), siplib.ispyowned(evt3)  
        #del evt1, evt2
        #print 'deleted'
        #evt3.Destroy()
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
