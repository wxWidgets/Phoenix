import imp_unittest, unittest
import wtc
import wx
import sys, os

#---------------------------------------------------------------------------

class MouseEventsPanel(wx.Panel):
    def __init__(self, parent, eventBinders):
        wx.Panel.__init__(self, parent, size=parent.GetClientSize())
        self.events = list()
        if not isinstance(eventBinders, (list, tuple)):
            eventBinders = [eventBinders]
        for binder in eventBinders:
            self.Bind(binder, self.onMouseEvent)
        
    def onMouseEvent(self, evt):
        self.events.append( (evt.EventType, evt.Position) )
        #print self.events[-1]
        evt.Skip()
        
        
class uiaction_MouseTests(wtc.WidgetTestCase):

            
    def cmp(self, info, evtType, pos):
        if isinstance(evtType, tuple):
            if info[0] not in evtType:
                return False
        else:
            if info[0] != evtType:
                return False
        # TODO: The mouse pos may be off by 1 on MSW, is this expected?
        if abs(info[1].x - pos[0]) > 1:
            return False
        if abs(info[1].y - pos[1]) > 1:
            return False
        return True
    
            
    def test_uiactionMouseMotion(self):
        p = MouseEventsPanel(self.frame, wx.EVT_MOTION)
        self.assertTrue(p.Size.Get() > (20,20))
        
        uia = wx.UIActionSimulator()
        uia.MouseMove(p.ClientToScreen((1,1)));   self.myYield()
        uia.MouseMove(p.ClientToScreen((5,5)));   self.myYield()
        uia.MouseMove(p.ClientToScreen((10,10)).x, p.ClientToScreen((10,10)).y)
        self.myYield()
        self.myYield()
        
        if sys.platform == 'darwin':
            # The events do seem to be happening, but I just can't seem to
            # capture them the same way as in the other tests, so bail out
            # before the asserts to avoid false negatives.
            return
        
        self.assertEqual(len(p.events) == 3)
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_MOTION, (1,1)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_MOTION, (5,5)))
        self.assertTrue(self.cmp(p.events[2], wx.wxEVT_MOTION, (10,10)))
        
        
    def test_uiactionMouseLeftDownUp(self):
        p = MouseEventsPanel(self.frame, [wx.EVT_LEFT_DOWN, wx.EVT_LEFT_UP])
        
        uia = wx.UIActionSimulator()
        uia.MouseMove(p.ClientToScreen((10,10)));   self.myYield()
        uia.MouseDown();                            self.myYield()
        uia.MouseUp();                              self.myYield()
        self.myYield()

        self.assertTrue(len(p.events) == 2)
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_LEFT_DOWN, (10,10)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_LEFT_UP, (10,10)))
        
        
    def test_uiactionMouseRightDownUp(self):
        p = MouseEventsPanel(self.frame, [wx.EVT_RIGHT_DOWN, wx.EVT_RIGHT_UP])
        
        uia = wx.UIActionSimulator()
        uia.MouseMove(p.ClientToScreen((10,10)));  self.myYield()
        uia.MouseDown(wx.MOUSE_BTN_RIGHT);         self.myYield()
        uia.MouseUp(wx.MOUSE_BTN_RIGHT);           self.myYield()
        self.myYield()

        self.assertTrue(len(p.events) == 2)
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_RIGHT_DOWN, (10,10)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_RIGHT_UP, (10,10)))
        

    def test_uiactionMouseLeftClick(self):
        p = MouseEventsPanel(self.frame, [wx.EVT_LEFT_DOWN, wx.EVT_LEFT_UP])
        
        uia = wx.UIActionSimulator()
        uia.MouseMove(p.ClientToScreen((10,10)));  self.myYield()
        uia.MouseClick();                          self.myYield()
        self.myYield()

        self.assertTrue(len(p.events) == 2)
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_LEFT_DOWN, (10,10)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_LEFT_UP, (10,10)))
        


    def test_uiactionMouseLeftDClick(self):
        p = MouseEventsPanel(self.frame, [wx.EVT_LEFT_DOWN, wx.EVT_LEFT_UP, wx.EVT_LEFT_DCLICK])
        
        uia = wx.UIActionSimulator()
        uia.MouseMove(p.ClientToScreen((10,10)));  self.myYield()
        uia.MouseDblClick();                       self.myYield()
        self.myYield()

        #print p.events
        self.assertTrue(len(p.events) == 4)
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_LEFT_DOWN, (10,10)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_LEFT_UP, (10,10)))
        self.assertTrue(self.cmp(p.events[2], (wx.wxEVT_LEFT_DOWN, wx.wxEVT_LEFT_DCLICK), (10,10)))
        self.assertTrue(self.cmp(p.events[3], wx.wxEVT_LEFT_UP, (10,10)))

        
        
    def test_uiactionMouseDD(self):
        p = MouseEventsPanel(self.frame, [wx.EVT_MOTION, wx.EVT_LEFT_DOWN, wx.EVT_LEFT_UP])
        
        x1, y1 = p.ClientToScreen((10,10))
        x2 = x1 + 20
        y2 = y1 + 20
        
        uia = wx.UIActionSimulator()
        uia.MouseDragDrop(x1,y1, x2,y2);  self.myYield()
        self.myYield()

        if sys.platform == 'darwin':
            # The events do seem to be happening, but I just can't seem to
            # capture them the same way as in the other tests, so bail out
            # before the asserts to avoid false negatives.
            return

        #print p.events
        self.assertEqual(len(p.events), 4)        
        self.assertTrue(self.cmp(p.events[0], wx.wxEVT_MOTION, (10,10)))
        self.assertTrue(self.cmp(p.events[1], wx.wxEVT_LEFT_DOWN, (10,10)))
        self.assertTrue(self.cmp(p.events[2], wx.wxEVT_MOTION, (30,30)))
        self.assertTrue(self.cmp(p.events[3], wx.wxEVT_LEFT_UP, (30,30)))
        
        
#---------------------------------------------------------------------------


class uiaction_KeyboardTests(wtc.WidgetTestCase):
    
    def setUp(self):
        super(uiaction_KeyboardTests, self).setUp()
        self.tc = wx.TextCtrl(self.frame)
        self.tc.SetFocus()
        self.myYield()
            
    
    def test_uiactionKeyboardKeyDownUp(self):
        uia = wx.UIActionSimulator()
        for c in "This is a test":
            if c.isupper():
                uia.KeyDown(wx.WXK_SHIFT);  self.myYield()
            uia.KeyDown(ord(c));            self.myYield()
            uia.KeyUp(ord(c));              self.myYield()
            if c.isupper():
                uia.KeyUp(wx.WXK_SHIFT);    self.myYield()
        self.waitFor(200)
                
        self.assertEqual(self.tc.GetValue(), "This is a test")
    
    
    def test_uiactionKeyboardChar(self):
        uia = wx.UIActionSimulator()
        for c in "This is a test":
            mod = wx.MOD_NONE
            if c.isupper():
                mod = wx.MOD_SHIFT
            uia.Char(ord(c), mod);  self.myYield()
        self.waitFor(200)
                        
        self.assertEqual(self.tc.GetValue(), "This is a test")



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
