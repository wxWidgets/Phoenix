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
        sound = wx.adv.Sound(opj('data/anykey.wav'))
        self.log.write("before Play...\n")
        sound.Play(wx.adv.SOUND_SYNC)
        self.log.write("...after Play\n")


    def OnButton2(self, evt):
        if True:
            sound = wx.adv.Sound(opj('data/plan.wav'))
        else:
            # sounds can also be loaded from a buffer object
            with open(opj('data/plan.wav'), 'rb') as fid:
                data = fid.read()
            sound = wx.adv.Sound()
            sound.CreateFromData(data)

        self.log.write("before Play...\n")
        sound.Play(wx.adv.SOUND_ASYNC)
        # On Windows, a sound loaded from a buffer can't be deleted while
        # it's playing, so keep a reference to it
        self.sound = sound
        self.log.write("...after Play\n")


    def OnSelectSound(self, evt):
        dlg = wx.FileDialog(wx.GetTopLevelParent(self),
                            "Choose a sound file",
                            wildcard="WAV files (*.wav)|*.wav",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # A shortcut for creating a wx.adv.Sound and playing it
            ok = wx.adv.Sound.PlaySound(dlg.GetPath(), wx.adv.SOUND_SYNC)
            self.log.write("PlaySound returned %s\n" % ok)
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
