#!/usr/bin/env python

import wx
import wx.dataview as dv


#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent)

        # create the treectrl
        self.dvtc = dvtc = dv.DataViewTreeCtrl(self)

        isz = (16,16)
        il = wx.ImageList(*isz)
        fldridx     = il.Add(wx.ArtProvider.GetIcon(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetIcon(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider.GetIcon(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        dvtc.SetImageList(il)

        self.root = dvtc.AppendContainer(dv.NullDataViewItem,
                                         "The Root Item",
                                         fldridx, fldropenidx)
        for x in range(15):
            child = dvtc.AppendContainer(self.root, "Item %d" % x,
                                         fldridx, fldropenidx)

            for y in range(5):
                last = dvtc.AppendContainer(
                    child, "item %d-%s" % (x, chr(ord("a")+y)),
                    fldridx, fldropenidx)

                for z in range(5):
                    item = dvtc.AppendItem(
                        last, "item %d-%s-%d" % (x, chr(ord("a")+y), z),
                        fileidx)

        # Set the layout so the treectrl fills the panel
        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(dvtc, 1, wx.EXPAND)



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewTreeCtrl</center></h2>

The DataViewTreeCtrl class is much like the traditional wx.TreeCtrl,
in that it stores all items itself and all access to the data is
through the tree ctrl's API. However it is derived from DataViewCtrl
and uses a model class internally, so it also has many of the benefits
of the data view classes available as well.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

