#!/usr/bin/env python

import wx
import wx.dataview as dv

#----------------------------------------------------------------------

# Reuse the music data in the ListCtrl sample
import ListCtrl
musicdata = sorted(ListCtrl.musicdata.items())
#musicdata.sort()
musicdata = [[str(k)] + list(v) for k,v in musicdata]


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # create the listctrl
        self.dvlc = dvlc = dv.DataViewListCtrl(self)

        # Give it some columns.
        # The ID col we'll customize a bit:
        dvlc.AppendTextColumn('id', width=40)
        dvlc.AppendTextColumn('artist', width=170)
        dvlc.AppendTextColumn('title', width=260)
        dvlc.AppendTextColumn('genre', width=80)

        # Load the data. Each item (row) is added as a sequence of values
        # whose order matches the columns
        for itemvalues in musicdata:
            dvlc.AppendItem(itemvalues)

        # Set the layout so the listctrl fills the panel
        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(dvlc, 1, wx.EXPAND)



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewListCtrl</center></h2>

The DataViewListCtrl class is much like the traditional wx.ListCtrl in report
mode, in that it stores all items itself and all access to the data is through
the list ctrl's API. However it is derived from DataViewCtrl and uses a model
class internally, so it also has many of the benefits of the data view classes
available as well.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

