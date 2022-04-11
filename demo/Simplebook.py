#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPage(wx.Panel):
    def __init__(self, parent, onNextPage, colour=None, title=None, text=None, extra=None):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        if colour:
            self.SetBackgroundColour(colour)

        if title:
            st = wx.StaticText(self, label=title)
            f = st.GetFont()
            f.SetPointSize(f.GetPointSize()+6)
            f.SetWeight(wx.FONTWEIGHT_BOLD)
            st.SetFont(f)
            vbox.Add(st, 0, wx.BOTTOM, 10)

        if text:
            st = wx.StaticText(self, label=text)
            vbox.Add(st, 0, wx.BOTTOM, 10)

        if extra:
            extra(self, vbox)

        vbox.AddStretchSpacer()

        btn = wx.Button(self, label="Next Page")
        vbox.Add(btn, 0, wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, onNextPage, btn)

        outer_sizer = wx.BoxSizer()
        outer_sizer.Add(vbox, 1, wx.EXPAND|wx.ALL, 15)
        self.SetSizer(outer_sizer)





class TestSimplebook(wx.Simplebook):
    def __init__(self, parent):
        wx.Simplebook.__init__(self, parent)

        self.showEffect = wx.SHOW_EFFECT_NONE
        self.hideEffect = wx.SHOW_EFFECT_NONE
        self.showTimeout = 0
        self.hideTimeout = 0

        self.DoSetEffects()

        page = TestPage(self, self.OnNextPage,
                        'sky blue', 'Page 1 of 4', text="""\
A wx.Simplebook is a notebook-like control that has no tabs or any other way
for the user to be able to select which page is to be shown. Page selection is
totally controlled by the application. For this example we are providing a
button to switch to the next page in the stack.""",
                        extra=self.MakeOptionsControls
                        )
        self.AddPage(page, '')

        page = TestPage(self, self.OnNextPage, 'pink', 'Page 2 of 4',
                        extra=self.MakeBackHomeButton)
        self.AddPage(page, '')

        page = TestPage(self, self.OnNextPage, 'medium aquamarine', 'Page 3 of 4',
                        extra=self.MakeBackHomeButton)
        self.AddPage(page, '')

        page = TestPage(self, self.OnNextPage, 'orchid', 'Page 4 of 4',
                        'Clicking "Next Page" will cycle back to the first page.',
                        extra=self.MakeBackHomeButton)
        self.AddPage(page, '')


    def MakeOptionsControls(self, panel, vbox):
        fgs = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        effects = [ 'wx.SHOW_EFFECT_NONE',
                    'wx.SHOW_EFFECT_ROLL_TO_LEFT',
                    'wx.SHOW_EFFECT_ROLL_TO_RIGHT',
                    'wx.SHOW_EFFECT_ROLL_TO_TOP ',
                    'wx.SHOW_EFFECT_ROLL_TO_BOTTOM',
                    'wx.SHOW_EFFECT_SLIDE_TO_LEFT',
                    'wx.SHOW_EFFECT_SLIDE_TO_RIGHT',
                    'wx.SHOW_EFFECT_SLIDE_TO_TOP',
                    'wx.SHOW_EFFECT_SLIDE_TO_BOTTOM',
                    'wx.SHOW_EFFECT_BLEND',
                    'wx.SHOW_EFFECT_EXPAND',
                    ]

        showEffectChoice = wx.Choice(panel, choices=effects)
        showTimeoutSpin = wx.SpinCtrl(panel, initial=0, max=1000)
        hideEffectChoice = wx.Choice(panel, choices=effects)
        hideTimeoutSpin = wx.SpinCtrl(panel, initial=0, max=1000)

        fgs.Add(wx.StaticText(panel, -1, "Show Effect:"))
        fgs.Add(showEffectChoice)
        fgs.Add(wx.StaticText(panel, -1, "Show Timeout (ms):"))
        fgs.Add(showTimeoutSpin)

        fgs.AddSpacer(10)
        fgs.AddSpacer(10)

        fgs.Add(wx.StaticText(panel, -1, "Hide Effect:"))
        fgs.Add(hideEffectChoice)
        fgs.Add(wx.StaticText(panel, -1, "Hide Timeout (ms):"))
        fgs.Add(hideTimeoutSpin)

        vbox.Add(fgs, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        self.Bind(wx.EVT_CHOICE, self.OnShowEffectChoice, showEffectChoice)
        self.Bind(wx.EVT_CHOICE, self.OnHideEffectChoice, hideEffectChoice)
        self.Bind(wx.EVT_SPINCTRL, self.OnShowTimeoutSpin, showTimeoutSpin)
        self.Bind(wx.EVT_SPINCTRL, self.OnHideTimeoutSpin, hideTimeoutSpin)


    def MakeBackHomeButton(self, panel, vbox):
        btn = wx.Button(panel, -1, 'Back to page 1')
        self.Bind(wx.EVT_BUTTON, self.OnBackHome, btn)
        vbox.AddSpacer(75)
        vbox.Add(btn)


    def OnNextPage(self, evt):
        current = self.GetSelection()
        current += 1
        if current >= self.GetPageCount():
            current = 0
        self.ChangeSelection(current)


    def OnBackHome(self, evt):
        self.ChangeSelection(0)


    def OnShowEffectChoice(self, evt):
        self.showEffect = eval(evt.GetString())
        self.DoSetEffects()


    def OnHideEffectChoice(self, evt):
        self.hideEffect = eval(evt.GetString())
        self.DoSetEffects()


    def OnShowTimeoutSpin(self, evt):
        self.showTimeout = evt.GetEventObject().GetValue()
        self.DoSetEffects()

    def OnHideTimeoutSpin(self, evt):
        self.hideTimeout = evt.GetEventObject().GetValue()
        self.DoSetEffects()


    def DoSetEffects(self):
        self.SetEffects(self.showEffect, self.hideEffect)
        self.SetEffectsTimeouts(self.showTimeout, self.hideTimeout)



#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        book = TestSimplebook(self)
        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(book, 1, wx.EXPAND)


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>Simplebook</center></h2>

A wx.Simplebook is a notebook-like control that has no tabs or
any other way for the user to be able to select which page is to
be shown. Page selection is totally controlled by the application.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

