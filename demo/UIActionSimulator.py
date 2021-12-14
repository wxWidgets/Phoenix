#!/usr/bin/env python

import wx
import wx.lib.buttons as buttons

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.recordingKeys = False
        self.stopwatchKeys = wx.StopWatch()
        self.uisim = wx.UIActionSimulator()


        # create widgets and bind events
        keyLabel = wx.StaticText(self, -1, "Key Events")
        keyLabel.SetFont(wx.FFont(18, wx.SWISS, wx.FONTFLAG_BOLD))

        self.txt = wx.TextCtrl(self, size=(300,-1))
        self.txt.Bind(wx.EVT_KEY_DOWN, self.OnTxtKeyDown)
        self.txt.Bind(wx.EVT_KEY_UP, self.OnTxtKeyUp)

        self.recordBtn = buttons.GenToggleButton(self, -1, "Record")
        self.Bind(wx.EVT_BUTTON, self.OnToggleRecordKeys, self.recordBtn)
        self.recordBtn.SetToolTip(
            "Click this button and then type some keys in the\n"
            "textctrl.  Click here again when done.")

        self.playbackKeysBtn = buttons.GenButton(self, -1, "Playback")
        self.Bind(wx.EVT_BUTTON, self.OnPlaybackKeys, self.playbackKeysBtn)
        self.playbackKeysBtn.SetToolTip(
            "Record some key events and then click here to\n"
            "replay the recorded events.")
        self.playbackKeysBtn.Disable()


        # create the layout
        gbs = wx.GridBagSizer(10,10)
        gbs.Add(keyLabel, (0,0), span=(1,2))
        gbs.Add(self.txt, (1,1), span=(1,2))
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add(self.recordBtn)
        btnsizer.Add((10,10))
        btnsizer.Add(self.playbackKeysBtn)
        gbs.Add(btnsizer, (2,1), span=(1,2))

        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(gbs, 1, wx.EXPAND|wx.ALL, 20)


    def OnToggleRecordKeys(self, evt):
        self.recordingKeys = not self.recordingKeys
        if self.recordingKeys:
            self.recordBtn.SetLabel('Recording')
            self.keyEvents = list()
            self.stopwatchKeys.Start()
            self.playbackKeysBtn.Disable()
            self.txt.Clear()
            self.txt.SetFocus()
        else:
            self.playbackKeysBtn.Enable()
            self.recordBtn.SetLabel('Record')


    def OnPlaybackKeys(self, evt):
        self._playbackEvents = self.keyEvents[:]  # make a copy so we can pop()
        if self._playbackEvents:
            self.playbackKeysBtn.Disable()
            self.txt.Clear()
            self.txt.SetFocus()
            self._setNextKeyEvent()


    def _playbackKey(self, evtType, key, modifiers):
        if evtType == 'down':
            self.uisim.KeyDown(key, modifiers)
        elif evtType == 'up':
            self.uisim.KeyUp(key, modifiers)

        if self._playbackEvents:
            self._setNextKeyEvent()
        else:
            self.playbackKeysBtn.Enable()


    def _setNextKeyEvent(self):
        evtType, key, modifiers, milli = self._playbackEvents.pop(0)
        milli = max(milli//2, 1) # play back faster than it was recorded
        print(evtType, key, modifiers, milli)
        wx.CallLater(milli, self._playbackKey, evtType, key, modifiers)


    def _onKeyEvent(self, evt, evtType):
        evt.Skip()
        if not self.recordingKeys:
            return
        evtInfo = ( evtType,
                    evt.KeyCode,
                    evt.GetModifiers(),
                    self.stopwatchKeys.Time(),
                    )
        self.keyEvents.append(evtInfo)
        self.stopwatchKeys.Start()


    def OnTxtKeyDown(self, evt):
        self._onKeyEvent(evt, 'down')

    def OnTxtKeyUp(self, evt):
        self._onKeyEvent(evt, 'up')



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    try:
        uisim = wx.UIActionSimulator()
        win = TestPanel(nb, log)
        return win
    except NotImplementedError:
        from wx.lib.msgpanel import MessagePanel
        win = MessagePanel(nb,
              "This build of wxWidgets does not include the \n"
              "wx.UIActionSimulator implementation.",
              "Sorry", wx.ICON_WARNING)
        return win


#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>UIActionSimulator</center></h2>

wx.UIActionSimulator is a class that facilitates the injection of
mouse or keyboard events into the application's message queue.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

