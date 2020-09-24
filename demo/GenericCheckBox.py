#!/usr/bin/env python

import wx
import wx.lib.checkbox as CB

#----------------------------------------------------------------------

class TestPanel(wx.Panel, CB.DefineNativeCheckBoxBitmapsMixin):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        # Make a couple Generic CheckBoxes.
        cb1 = CB.GenCheckBox(self, label="PurePython Checkbox1", pos=(10, 10))
        cb2 = CB.GenCheckBox(self, label="PurePython Checkbox2", pos=(10, 50))
        cb1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        cb2.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        cb2.SetForegroundColour(wx.GREEN)
        cb2.SetBackgroundColour(wx.BLACK)
        sizer = wx.BoxSizer()
        sizer.Add(cb1, 0, wx.ALL, 8)
        sizer.Add(cb2, 0, wx.ALL, 8)


        # If you like to tinker around with drawing the bitmap images
        # on another widget. Ex: Maybe in a StyledTextCtrl Margin or TreeCtrl.
        try:
            self.DefineNativeCheckBoxBitmaps()
            self.checkbox_bitmaps = self.GetNativeCheckBoxBitmaps()
        except Exception as exc:
            self.log.WriteText("FAILED defining native checkbox bitmaps!")
            self.checkbox_bitmaps = None

        if self.checkbox_bitmaps:
            for bmp in self.checkbox_bitmaps:
                sb = wx.StaticBitmap(self, -1, bmp)
                sizer.Add(sb, 0, wx.ALL, 8)

        self.SetSizer(sizer)

    def OnCheckBox(self, event):
        evtObj = event.GetEventObject()
        label = evtObj.GetLabel()
        checked = evtObj.IsChecked()
        self.log.WriteText("GenCheckBox Clicked: %s %s\n" % (label, checked))


#----------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#----------------------------------------------------------------------


overview = CB.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

