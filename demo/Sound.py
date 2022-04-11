#!/usr/bin/env python

import wx
import wx.adv
from Main import opj

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        b = wx.Button(self, -1, "Play Sound 1 (sync)", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnButton1, b)

        b = wx.Button(self, -1, "Play Sound 2 (async)", (25, 65))
        self.Bind(wx.EVT_BUTTON, self.OnButton2, b)

        b = wx.Button(self, -1, "Select .WAV file", (25, 105))
        self.Bind(wx.EVT_BUTTON, self.OnSelectSound, b)


    def OnButton1(self, evt):
        try:
            sound = wx.adv.Sound(opj('data/anykey.wav'))
            self.log.write("before Play...\n")
            sound.Play(wx.adv.SOUND_SYNC)
            self.log.write("...after Play\n")
        except NotImplementedError as v:
            wx.MessageBox(str(v), "Exception Message")


    def OnButton2(self, evt):
        try:
            if True:
                sound = wx.adv.Sound(opj('data/plan.wav'))
            else:
                # sounds can also be loaded from a buffer object
                with open(opj('data/plan.wav'), 'rb') as fid:
                    data = fid.read()
                sound = wx.SoundFromData(data)

            self.log.write("before Play...\n")
            sound.Play(wx.adv.SOUND_ASYNC)
            self.sound = sound  # save a reference (This shouldn't be needed, but there seems to be a bug...)
            # wx.YieldIfNeeded()
            self.log.write("...after Play\n")
        except NotImplementedError as v:
            wx.MessageBox(str(v), "Exception Message")


    def OnSelectSound(self, evt):
        dlg = wx.FileDialog(wx.GetTopLevelParent(self),
                            "Choose a sound file",
                            wildcard="WAV files (*.wav)|*.wav",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                #sound = wx.adv.Sound(dlg.GetPath(), wx.SOUND_SYNC)
                #sound.Play()

                # another way to do it.
                wx.adv.Sound.PlaySound(dlg.GetPath(), wx.adv.SOUND_SYNC)

            except NotImplementedError as v:
                wx.MessageBox(str(v), "Exception Message")
        dlg.Destroy()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2>Sound</h2>
This class represents a short wave file, in Windows WAV format, that can
be stored in memory and played.
<p>
This demo offers two examples, both driven by buttons, but obviously the event
that drives the playing of the sound can come from anywhere.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
