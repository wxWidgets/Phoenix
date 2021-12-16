#!/usr/bin/env python

import time

import wx

npts = 100000

def TestLinesFromBuffer(dc, log):
    global npts
    try:
        import numpy as np
        start = time.time()

        w, h = dc.GetSize()

        vs = np.linspace(0, 1, npts).reshape((npts, 1))

        x1 = np.cos(vs * 12 * np.pi) * w/2 * vs + w/2
        x2 = np.cos(vs * 16 * np.pi) * w/2 * vs + w/2
        y1 = np.sin(vs * 12 * np.pi) * w/2 * vs + h/2
        y2 = np.sin(vs * 16 * np.pi) * w/2 * vs + h/2
        

        # Data has to be the same size as a C integer
        pts1 = np.append(x1, y1, 1).astype('intc')
        pts2 = np.append(x2, y2, 1).astype('intc')

        dc.SetPen(wx.BLACK_PEN)
        t1 = time.time()
        dc.DrawLines(pts1)
        t2 = time.time()
        
        dc.SetPen(wx.RED_PEN)
        t3 = time.time()
        dc.DrawLinesFromBuffer(pts2)
        t4 = time.time()
        
        log.write("%s pts: %s seconds with DrawLines %s seconds with DrawLinesFromBuffer\n" % (npts, t2 - t1, t4 - t3))

    except ImportError:
        log.write("Couldn't import numpy")
        pass



# Class used for all the various sample pages; the mechanics are the same
# for each one with regards to the notebook. The only difference is
# the function we use to draw on it.
class DrawPanel(wx.Panel):
    def __init__(self, parent, drawFun, log):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(wx.WHITE)

        self.log = log
        self.drawFun = drawFun
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnSize(self, evt):
        self.Refresh()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        self.drawFun(dc,self.log)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    global npts
    
    panel = wx.Panel(nb, -1)
    vsizer = wx.BoxSizer(wx.VERTICAL)
    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    hsizer.Add(wx.StaticText(panel, -1, "# of Points"), 0, wx.ALIGN_CENTER|wx.ALL, 5)
    npts_ctrl = wx.TextCtrl(panel, -1, str(npts))
    hsizer.Add(npts_ctrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)
    
    button = wx.Button(panel, -1, "Refresh")
    hsizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
    vsizer.Add(hsizer, 0, wx.ALIGN_CENTER, 0)
    
    win = DrawPanel(panel, TestLinesFromBuffer, log)
    vsizer.Add(win, 1, wx.GROW, 0)
    panel.SetSizer(vsizer)
    
    def update_npts(evt):
        global npts
        
        val = npts_ctrl.GetValue()
        try:
            npts = int(val)
        except ValueError:
            log.write("Error converting %s to an int" % (val))
        win.Refresh()
    button.Bind(wx.EVT_BUTTON, update_npts)
    
    return panel

#----------------------------------------------------------------------


overview = """\

The DrawLinesFromBuffer function has been added to wx.DC to provide 
a way to draw directly from a numpy array or other object that implements
the python buffer protocol.  

<pre>
    DrawLinesFromBuffer(pyBuff)
</pre>

The buffer object needs to provide an array of C integers organized as 
x, y point pairs.  The size of a C integer is platform dependent.
With numpy, the intc data type will provide the appropriate element size.

If called with an object that doesn't support
the python buffer protocol, or if the underlying element size does not
match the size of a C integer, a TypeError exception is raised.  If 
the buffer provided has float data with the same element size as a 
C integer, no error will be raised, but the lines will not be drawn
in the appropriate places.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

