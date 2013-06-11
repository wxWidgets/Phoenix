
import  wx
from wx import html

#----------------------------------------------------------------------

# The wx.VListBox is much like a regular wx.ListBox except you draw the
# items yourself and the items can vary in height.
class MyVListBox(wx.VListBox):

    # This method must be overridden.  When called it should draw the
    # n'th item on the dc within the rect.  How it is drawn, and what
    # is drawn is entirely up to you.
    def OnDrawItem(self, dc, rect, n):
        if self.GetSelection() == n:
            c = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        else:
            c = self.GetForegroundColour()
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(c)
        dc.DrawLabel(self._getItemText(n), rect,
                     wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

    # This method must be overridden.  It should return the height
    # required to draw the n'th item.
    def OnMeasureItem(self, n):
        height = 0
        for line in self._getItemText(n).split('\n'):
            w, h = self.GetTextExtent(line)
            height += h
        return height + 5


    # These are also overridable:
    #
    # OnDrawSeparator(dc, rect, n)
    #   Draw a separator between items.  Note that rect may be reduced
    #   in size if desired so OnDrawItem gets a smaller rect.
    #
    # OnDrawBackground(dc, rect, n)
    #   Draw the background and maybe a border if desired.


    def _getItemText(self, item):
        if item % 2 == 0:
            return "This is item# %d" % item
        else:
            return "This is item# %d\n with an extra line" % item

#----------------------------------------------------------------------

# The wx.HtmlListBox derives from wx.VListBox, but draws each item
# itself as a wx.HtmlCell.
class MyHtmlListBox(wx.HtmlListBox):

    def __init__(self, *args, **kw):
        self.log = kw.pop('log')
        wx.HtmlListBox.__init__(self, *args, **kw)

    def OnGetItem(self, n):
        if n == 1:
            return """<table border="0" cellpadding="0" cellspacing="0">
<tr>
    <td width="33">col 1</td>
    <td width="75">Lorem ipsum <a href="http://www.wxpython.org">dolor</a>
    sit amet, consectetuer adipiscing elit.</td>
    <td width="300">foobar</td>
</tr>
</table>"""
        if n % 2 == 0:
            return "This is item# <b>%d</b>" % n
        else:
            return "This is item# <b>%d</b> <br>Any <font color='RED'>HTML</font> is okay." % n

    def OnLinkClicked(self, n, linkinfo):
        self.log.WriteText('OnLinkClicked: %s\n' % linkinfo.GetHref())
        #there's a bug in the wxPython wrapper as of 2.8.7.1
        #super(MyHtmlListBox, self).OnLinkClicked(n, linkinfo)


#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        spacer = 50

        vlb = MyVListBox(self, -1, size=(150, 250), style=wx.BORDER_SUNKEN)
        vlb.SetItemCount(50)
        vlb.SetSelection(0)
        vlb.SetFocus()
        vlbSizer = wx.BoxSizer(wx.VERTICAL)
        vlbSizer.Add((spacer, spacer))
        vlbSizer.Add(wx.StaticText(self, -1, "wx.VListBox"), 0, 5, wx.ALL)
        vlbSizer.Add(vlb)

        hlb = MyHtmlListBox(self, -1, size=(150, 250), style=wx.BORDER_SUNKEN,
                            log=log)
        hlb.SetItemCount(50)
        hlb.SetSelection(0)
        hlbSizer = wx.BoxSizer(wx.VERTICAL)
        hlbSizer.Add((spacer, spacer))
        hlbSizer.Add(wx.StaticText(self, -1, "wx.HtmlListBox"), 0, 5, wx.ALL)
        hlbSizer.Add(hlb)

        self.Bind(html.EVT_HTML_CELL_CLICKED, self.OnCellClicked, hlb )
        self.Bind(html.EVT_HTML_CELL_HOVER, self.OnCellMouseHover, hlb )
        #there's a bug in the wxPython wrapper as of 2.8.7.1
        #self.Bind(html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked, hlb )

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((spacer, spacer))
        sizer.Add(vlbSizer)
        sizer.Add((spacer, spacer))
        sizer.Add((spacer, spacer))
        sizer.Add(hlbSizer)

        self.SetSizer(sizer)

    #there's a bug in the wxPython wrapper as of 2.8.7.1
    #def OnLinkClicked(self, event):
    #    linkinfo = event.GetLinkInfo()
    #    self.log.WriteText('OnLinkClicked: %s\n' % linkinfo.GetHref())
    #
    def OnCellMouseHover(self, event):
        cell = event.GetCell()
        self.log.WriteText('OnCellMouseHover: %s\n' % (cell))
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
            self.log.WriteText('     %s\n' % cell.ConvertToText(sel))
        event.Skip()

    def OnCellClicked(self, event):
        cell = event.GetCell()
        self.log.WriteText('OnCellClicked: %s\n' % (cell))
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
            self.log.WriteText('     %s\n' % cell.ConvertToText(sel))
        event.Skip()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.VListBox and wx.HtmlListBox</center></h2>
<hr>

The "V" in wxVListBox stands for both "virtual" because it can have an
unlimited number of items since it doesn't store them itself, and
"variable" since items can vary in height.  It has much the same
interface as wxListBox and also emits the same events so you can use
the same EVT_LISTBOX function to connect a handler.
<p>

The wx.HtmlListBox derives from wx.VListBox, but draws each item itself
as a wx.HtmlCell.  This means that you just need to provide a snippet
of HTML for each item when requested.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
