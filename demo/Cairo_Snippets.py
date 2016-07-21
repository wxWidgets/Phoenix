#!/usr/bin/env python

import wx

try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False

from math import pi as M_PI  # used by many snippets
from snippets import snip_list, snippet_normalize
from Main import opj, DemoCodeEditor

#----------------------------------------------------------------------

# TODO:  Add the ability for the user to edit and render their own snippet

class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SIMPLE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.curr_snippet = ''


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)

        if self.curr_snippet:
            width, height = self.GetClientSize()
            cr = wx.lib.wxcairo.ContextFromDC(dc)
            exec(self.curr_snippet, globals(), locals())


    def SetSnippet(self, text):
        self.curr_snippet = text
        self.Refresh()



class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.lb = wx.ListBox(self, choices=snip_list)
        self.canvas = DisplayPanel(self)
        self.editor = DemoCodeEditor(self, style=wx.BORDER_SIMPLE)
        self.editor.SetEditable(False)

        self.Bind(wx.EVT_LISTBOX, self.OnListBoxSelect, self.lb)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.lb, 0, wx.EXPAND)
        sizer.Add((15,1))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.canvas, 1, wx.EXPAND)
        vbox.Add((1, 15))
        vbox.Add(self.editor, 1, wx.EXPAND)
        sizer.Add(vbox, 1, wx.EXPAND)
        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 30)
        self.SetSizer(border)


    def OnListBoxSelect(self, evt):
        snippet_file = opj('snippets/%s.py' % evt.GetString())
        with open(snippet_file) as f:
            text = f.read()
        self.canvas.SetSnippet(text)
        self.editor.SetValue(text)


#----------------------------------------------------------------------

if not haveCairo:
    from wx.lib.msgpanel import MessagePanel
    def runTest(frame, nb, log):
        win = MessagePanel(
            nb, 'This demo requires either the PyCairo package or the\n'
                'cairocffi package, or there is some other unmet dependency.',
                'Sorry', wx.ICON_WARNING)
        return win
else:

    def runTest(frame, nb, log):
        win = TestPanel(nb, log)
        return win

#----------------------------------------------------------------------

if haveCairo:
    extra = "\n<h3>wx.lib.wxcairo</h3>\n%s" % (
        wx.lib.wxcairo.__doc__.replace('\n\n', '\n<p>'))
else:
    extra = '\n<p>See the docstring in the wx.lib.wxcairo module for details about installing dependencies.'


overview = """<html><body>
<h2><center>Cairo Integration</center></h2>

The wx.lib.wxcairo module provides a bit of glue that will allow you to
use the PyCairo or cairocffi packages to do Cairo drawing directly on wx.DC's.

<p> This sample draws the standard 'snippet' examples that come with
the PyCairo package, and a few others.  The C version of the samples
can be seen at http://cairographics.org/samples/

<p> In most snippets you'll see a call to a snippet_normalize()
function.  This is part of the demo and not part of Cairo.  It is
simply scaling the context such that the range of 0.0 to 1.0 is the
min(width, height) of the window in pixels.  In other words, it allows
the rendering code to use a range or 0.0 to 1.0 and it will always fit
in the drawing area.  (Try resizing the demo and reselecting a snippet
to see this.)

<pre>
def snippet_normalize(ctx, width, height):
    size = min(width, height)
    ctx.scale(size, size)
    ctx.set_line_width(0.04)
</pre>

%s
</body></html>
""" % extra



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

