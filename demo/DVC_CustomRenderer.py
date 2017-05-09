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


    def SetValue(self, value):
        #self.log.write('SetValue: %s' % value)
        self.value = value
        return True

    def GetValue(self):
        self.log.write('GetValue')
        return self.value

    def GetSize(self):
        # Return the size needed to display the value.  The renderer
        # has a helper function we can use for measuring text that is
        # aware of any custom attributes that may have been set for
        # this item.
        value = self.value if self.value else ""
        return self.GetTextExtent(value)


    def Render(self, rect, dc, state):
        #if state != 0:
        #    self.log.write('Render: %s, %d' % (rect, state))

        if not state & dv.DATAVIEW_CELL_SELECTED:
            # we'll draw a shaded background to see if the rect correctly
            # fills the cell
            dc.SetBrush(wx.Brush('light grey'))
            dc.SetPen(wx.TRANSPARENT_PEN)
            rect.Deflate(1, 1)
            dc.DrawRoundedRectangle(rect, 2)

        # And then finish up with this helper function that draws the
        # text for us, dealing with alignment, font and color
        # attributes, etc
        value = self.value if self.value else ""
        self.RenderText(value,
                        4,   # x-offset, to compensate for the rounded rectangles
                        rect,
                        dc,
                        state # wxDataViewCellRenderState flags
                        )
        return True


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
        c0 = self.dvc.AppendTextColumn("Id", 0, width=40)
        c0.Alignment = wx.ALIGN_RIGHT
        c0.MinWidth = 40

        # We'll use our custom renderer for these columns
        for title, col, width in [ ('Artist', 1, 170),
                                   ('Title', 2, 260),
                                   ('Genre', 3, 80)]:
            renderer = MyCustomRenderer(self.log, mode=dv.DATAVIEW_CELL_EDITABLE)
            #renderer.SetMode(dv.DATAVIEW_CELL_EDITABLE)
            column = dv.DataViewColumn(title, renderer, col, width=width)
            column.Alignment = wx.ALIGN_LEFT
            self.dvc.AppendColumn(column)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)



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
<h2><center>DemoName</center></h2>

Say something nice here

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

