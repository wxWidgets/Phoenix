#!/usr/bin/env python

"""
This demo attempts to override the C++ MainLoop and implement it
in Python.
"""

import time
import wx
import wx.lib.newevent as ne


##import os; raw_input('PID: %d\nPress enter...' % os.getpid())

GooEvent, EVT_GOO = ne.NewCommandEvent()

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300, 200))

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOVE, self.OnMove)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(EVT_GOO, self.OnGoo, id=123)

        self.count = 0

        panel = wx.Panel(self)
        sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        self.sizeCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(panel, -1, "Size:"))
        sizer.Add(self.sizeCtrl)

        self.posCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(panel, -1, "Pos:"))
        sizer.Add(self.posCtrl)

        self.idleCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(panel, -1, "Idle:"))
        sizer.Add(self.idleCtrl)

        btn = wx.Button(panel, label='PostEvent')
        sizer.Add(1,1)
        sizer.Add(btn)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        panel.SetSizer(border)


    def OnCloseWindow(self, event):
        self.Destroy()

    def OnIdle(self, event):
        self.idleCtrl.SetValue(str(self.count))
        self.count = self.count + 1

    def OnSize(self, event):
        size = event.GetSize()
        self.sizeCtrl.SetValue("%s, %s" % (size.width, size.height))
        event.Skip()

    def OnMove(self, event):
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

    def OnButton(self, evt):
        evt = GooEvent(id=123)
        wx.PostEvent(self, evt)

    def OnGoo(self, evt):
        print('got EVT_GOO')


#---------------------------------------------------------------------------

class MyEventLoop(wx.GUIEventLoop):
    def __init__(self):
        wx.GUIEventLoop.__init__(self)
        self.exitCode = 0
        self.shouldExit = False


    def DoMyStuff(self):
        # Do whatever you want to have done for each iteration of the event
        # loop. In this example we'll just sleep a bit to simulate something
        # real happening.
        time.sleep(0.05)


    def Run(self):
        # Set this loop as the active one. It will automatically reset to the
        # original evtloop when the context manager exits.
        with wx.EventLoopActivator(self):
            while True:

                self.DoMyStuff()

                # Generate and process idles events for as long as there
                # isn't anything else to do
                while not self.shouldExit and not self.Pending() and self.ProcessIdle():
                    pass

                if self.shouldExit:
                    break

                # Dispatch all the pending events
                self.ProcessEvents()

                # Currently on wxOSX Pending always returns true, so the
                # ProcessIdle above is not ever called. Call it here instead.
                if 'wxOSX' in wx.PlatformInfo:
                    self.ProcessIdle()

            # Process remaining queued messages, if any
            while True:
                checkAgain = False
                if wx.GetApp() and wx.GetApp().HasPendingEvents():
                    wx.GetApp().ProcessPendingEvents()
                    checkAgain = True
                if 'wxOSX' not in wx.PlatformInfo and self.Pending():
                    self.Dispatch()
                    checkAgain = True
                if not checkAgain:
                    break

        return self.exitCode


    def Exit(self, rc=0):
        self.exitCode = rc
        self.shouldExit = True
        self.OnExit()
        self.WakeUp()


    def ProcessEvents(self):
        if wx.GetApp():
            wx.GetApp().ProcessPendingEvents()

        if self.shouldExit:
            return False

        return self.Dispatch()





class MyApp(wx.App):

    def MainLoop(self):
        self.SetExitOnFrameDelete(True)
        self.mainLoop = MyEventLoop()
        self.mainLoop.Run()

    def ExitMainLoop(self):
        self.mainLoop.Exit()

    def OnInit(self):
        frame = MyFrame(None, -1, "This is a test")
        frame.Show(True)
        self.SetTopWindow(frame)

        #self.keepGoing = True
        return True


app = MyApp(False)
app.MainLoop()





