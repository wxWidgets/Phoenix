#!/usr/bin/env python

import wx
import wx.dataview

import images

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.tree = wx.dataview.TreeListCtrl(self, -1, style =
                                        wx.TR_DEFAULT_STYLE
                                        #| wx.TR_HAS_BUTTONS
                                        #| wx.TR_TWIST_BUTTONS
                                        #| wx.TR_ROW_LINES
                                        #| wx.TR_COLUMN_LINES
                                        #| wx.TR_NO_LINES
                                        | wx.TR_FULL_ROW_HIGHLIGHT
                                   )

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        smileidx    = il.Add(images.Smiles.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il

        # create some columns
        self.tree.AppendColumn("Main column")
        self.tree.AppendColumn("Column 1")
        self.tree.AppendColumn("Column 2")
        ##self.tree.SetMainColumn(0) # the one with the tree in it...
        self.tree.SetColumnWidth(0, 175)

        self.root = self.tree.InsertItem(self.tree.GetRootItem(), wx.dataview.TLI_FIRST, "The Root Item")

        self.tree.SetItemText(self.root, 1, "col 1 root")
        self.tree.SetItemText(self.root, 2, "col 2 root")
        self.tree.SetItemImage(self.root, closed=fldridx, opened=fldropenidx)


        for x in range(15):
            txt = "Item %d" % x
            child = self.tree.AppendItem(self.root, txt)
            self.tree.SetItemText(child, 1, txt + "(c1)")
            self.tree.SetItemText(child, 2, txt + "(c2)")
            self.tree.SetItemImage(child, closed=fldridx, opened=fldropenidx)

            for y in range(5):
                txt = "item %d-%s" % (x, chr(ord("a")+y))
                last = self.tree.AppendItem(child, txt)
                self.tree.SetItemText(last, 1, txt + "(c1)")
                self.tree.SetItemText(last, 2, txt + "(c2)")
                self.tree.SetItemImage(last, closed=fldridx, opened=fldropenidx)

                for z in range(5):
                    txt = "item %d-%s-%d" % (x, chr(ord("a")+y), z)
                    item = self.tree.AppendItem(last,  txt)
                    self.tree.SetItemText(item, 1, txt + "(c1)")
                    self.tree.SetItemText(item, 2, txt + "(c2)")
                    #TODO: Phoenix change selected to smiley
                    self.tree.SetItemImage(item, closed=fileidx, opened=smileidx)
                    ## self.tree.SetItemImage(item, fileidx, which = wx.TreeItemIcon_Normal)
                    ## self.tree.SetItemImage(item, smileidx, which = wx.TreeItemIcon_Selected)


        self.tree.Expand(self.root)

        ## self.tree.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)


    def OnActivate(self, event):
        self.log.write('OnActivate: %s' % self.tree.GetItemText(event.GetItem()))

    def OnRightUp(self, event):
        pos = event.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        if item:
            self.log.write('Flags: %s, Col:%s, Text: %s' %
                           (flags, col, self.tree.GetItemText(item, col)))

    def OnSize(self, event):
        self.tree.SetSize(self.GetSize())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>TreeListCtrl</center></h2>

The TreeListCtrl is essentially a wx.TreeCtrl with extra columns,
such that the look is similar to a wx.ListCtrl.

</body></html>
"""


if __name__ == '__main__':
    #raw_input("Press enter...")
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

