#
# A simple test to verify that the GIL is released while in long running
# wrappers like MainLoop, ShowModal, and PopupMenu so background threads can
# be allowed to run at those times.
#

import wx
import threading
import time
import random

print(wx.version())


class ThreadedTask(threading.Thread):
    def __init__(self, *args, **kw):
        threading.Thread.__init__(self, *args, **kw)
        self.counter = 0
        self.sleepTime = random.random()/2
        self.timeToDie = False

    def run(self):
        while not self.timeToDie:
            time.sleep(self.sleepTime)
            self.counter += 1
            print('thread: %5s count: %d' % (self.name, self.counter))



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="GIL Test")
        self.pnl = wx.Panel(self)
        btn = wx.Button(self.pnl, label='modal dialog', pos=(10,10))
        self.Bind(wx.EVT_BUTTON, self.onButton, btn)
        self.pnl.Bind(wx.EVT_CONTEXT_MENU, self.onShowMenu)
        btn = wx.Button(self.pnl, label='timed test', pos=(10, 60))
        self.Bind(wx.EVT_BUTTON, self.onOtherButton, btn)


    def onButton(self, evt):
        dlg = wx.Dialog(self, title='close this dialog', size=(300,150))
        dlg.ShowModal()
        dlg.Destroy()


    def onOtherButton(self, evt):
        # A simplistic benchmark test that times many repititions of some
        # simple operations so they can be tested with and without releasing
        # the GIL
        start = time.time()
        reps = 100000
        for x in range(reps):
            s = wx.Size(100, 100)
            for n in range(10):
                s.DecBy(4,6)
            for n in range(10):
                s.IncBy(4,6)
        wx.MessageBox('%d reps performed in %f seconds' % (reps, time.time() - start),
                      'Results')


    def onShowMenu(self, evt):
        menu = wx.Menu()
        menu.Append(-1, 'one')
        menu.Append(-1, 'two')
        menu.Append(-1, 'three')
        self.pnl.PopupMenu(menu)
        menu.Destroy()



threads = [ ThreadedTask(name='one'), ThreadedTask(name='two'), ThreadedTask(name='three') ]
for t in threads:
    t.start()

app = wx.App()
frm = MainFrame()
frm.Show()
app.MainLoop()

for t in threads:
    t.timeToDie = True

