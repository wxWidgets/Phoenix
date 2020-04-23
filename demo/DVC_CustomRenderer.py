#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import wx.dataview as dv

#----------------------------------------------------------------------

class MyCustomRenderer(dv.DataViewCustomRenderer):
    def __init__(self, log, *args, **kw):
        dv.DataViewCustomRenderer.__init__(self, *args, **kw)
        self.log = log
        self.value = None
        self.EnableEllipsize(wx.ELLIPSIZE_END)


    def SetValue(self, value):
        #self.log.write('SetValue: %s' % value)
        self.value = value
        return True


    def GetValue(self):
        self.log.write('GetValue: {}'.format(value))
        return self.value


    def GetSize(self):
        # Return the size needed to display the value.  The renderer
        # has a helper function we can use for measuring text that is
        # aware of any custom attributes that may have been set for
        # this item.
        value = self.value if self.value else ""
        size = self.GetTextExtent(value)
        size += (2,2)
        #self.log.write('GetSize("{}"): {}'.format(value, size))
        return size


    def Render(self, rect, dc, state):
        #if state != 0:
        #    self.log.write('Render: %s, %d' % (rect, state))

        if not state & dv.DATAVIEW_CELL_SELECTED:
            # we'll draw a shaded background to see if the rect correctly
            # fills the cell
            dc.SetBrush(wx.Brush('#ffd0d0'))
            dc.SetPen(wx.TRANSPARENT_PEN)
            rect.Deflate(1, 1)
            dc.DrawRoundedRectangle(rect, 2)

        # And then finish up with this helper function that draws the
        # text for us, dealing with alignment, font and color
        # attributes, etc.
        value = self.value if self.value else ""
        self.RenderText(value,
                        0,   # x-offset
                        rect,
                        dc,
                        state # wxDataViewCellRenderState flags
                        )
        return True


    def ActivateCell(self, rect, model, item, col, mouseEvent):
        self.log.write("ActivateCell")
        return False


    # The HasEditorCtrl, CreateEditorCtrl and GetValueFromEditorCtrl
    # methods need to be implemented if this renderer is going to
    # support in-place editing of the cell value, otherwise they can
    # be omitted.

    def HasEditorCtrl(self):
        self.log.write('HasEditorCtrl')
        return True


    def CreateEditorCtrl(self, parent, labelRect, value):
        self.log.write('CreateEditorCtrl: %s' % labelRect)
        ctrl = wx.TextCtrl(parent,
                           value=value,
                           pos=labelRect.Position,
                           size=labelRect.Size)

        # select the text and put the caret at the end
        ctrl.SetInsertionPointEnd()
        ctrl.SelectAll()

        return ctrl


    def GetValueFromEditorCtrl(self, editor):
        self.log.write('GetValueFromEditorCtrl: %s' % editor)
        value = editor.GetValue()
        return value


    # The LeftClick and Activate methods serve as notifications
    # letting you know that the user has either clicked or
    # double-clicked on an item.  Implementing them in your renderer
    # is optional.

    def LeftClick(self, pos, cellRect, model, item, col):
        self.log.write('LeftClick')
        return False


    def Activate(self, cellRect, model, item, col):
        self.log.write('Activate')
        return False


#----------------------------------------------------------------------

# To help focus this sample on the custom renderer, we'll reuse the
# model class from another sample.
from DVC_IndexListModel import TestModel



class TestPanel(wx.Panel):
    def __init__(self, parent, log, model=None, data=None):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )

        # Create an instance of the model
        if model is None:
            self.model = TestModel(data, log)
        else:
            self.model = model
        self.dvc.AssociateModel(self.model)

        # Now we create some columns.
        col = self.dvc.AppendTextColumn("Id", 0, width=40)
        col.Alignment = wx.ALIGN_RIGHT
        col.MinWidth = 40

        col = self.dvc.AppendTextColumn("Artist", 1, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        col.Alignment = wx.ALIGN_LEFT

        renderer = MyCustomRenderer(self.log, mode=dv.DATAVIEW_CELL_EDITABLE)
        col = dv.DataViewColumn("Title", renderer, 2, width=260)
        col.Alignment = wx.ALIGN_LEFT
        self.dvc.AppendColumn(col)

        col = self.dvc.AppendTextColumn("Genre", 3, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        col.Alignment = wx.ALIGN_LEFT

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)


    def ShowMessage(self):
        msg = "This platform does not have good support for editing cells " \
              "which have a custom renderer, so the Title column's mode " \
              "will be set to DATAVIEW_CELL_INERT instead."
        wx.MessageBox(msg, "Custom Renderer Info", style=wx.OK|wx.ICON_INFORMATION)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    # Get the data from the ListCtrl sample to play with, converting it
    # from a dictionary to a list of lists, including the dictionary key
    # as the first element of each sublist.
    import ListCtrl
    musicdata = ListCtrl.musicdata.items()
    musicdata = sorted(musicdata)
    musicdata = [[str(k)] + list(v) for k,v in musicdata]

    win = TestPanel(nb, log, data=musicdata)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewCustomRenderer</center></h2>

This sample shows how to implement a renderer for drawing the cells in a
DataViewControl in a custom manner.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

