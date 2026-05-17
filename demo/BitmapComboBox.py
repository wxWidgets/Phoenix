#!/usr/bin/env python

import wx
import wx.adv

import images

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        wx.StaticText(self, pos=(25,5),  size=(200,-1), label="default style:")
        wx.StaticText(self, pos=(250,5), size=(200,-1), label="wx.CB_READONLY style:")

        bcb1 = wx.adv.BitmapComboBox(self, pos=(25,35),  size=(200,-1))
        bcb2 = wx.adv.BitmapComboBox(self, pos=(250,35), size=(200,-1), style=wx.CB_READONLY)

        for bcb in [bcb1, bcb2]:
            for x in range(12):
                name = 'LB%02d' % (x+1)
                obj = getattr(images, name)
                img = obj.GetImage()
                img.Rescale(20,20)
                bmp = img.ConvertToBitmap()
                bcb.Append('images.%s' % name, bmp, name)
            self.Bind(wx.EVT_COMBOBOX, self.OnCombo, bcb)

    def OnCombo(self, evt):
        bcb = evt.GetEventObject()
        idx = evt.GetInt()
        st  = bcb.GetString(idx)
        cd  = bcb.GetClientData(idx)
        self.log.write("EVT_COMBOBOX: Id %d, string '%s', clientData '%s'" % (idx, st, cd))


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.combo.BitmapComboBox</center></h2>

A combobox that displays a bitmap in front of the list items. It
currently only allows using bitmaps of one size, and resizes itself so
that a bitmap can be shown next to the text field.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

