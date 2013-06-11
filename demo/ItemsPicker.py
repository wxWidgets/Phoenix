import wx
from wx.lib.itemspicker import ItemsPicker, \
                               EVT_IP_SELECTION_CHANGED, \
                               IP_SORT_CHOICES, IP_SORT_SELECTED,\
                               IP_REMOVE_FROM_CHOICES

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self,-1,"ItemPicker styles")
        boxSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        self.sortChoices = wx.CheckBox(self,-1,'IP_SORT_CHOICES')
        boxSizer.Add(self.sortChoices)
        self.sortSelected = wx.CheckBox(self,-1,'IP_SORT_SELECTED')
        boxSizer.Add(self.sortSelected)
        self.removeFromChoices = wx.CheckBox(self,-1,'IP_REMOVE_FROM_CHOICES')
        boxSizer.Add(self.removeFromChoices)
        sizer.Add(boxSizer,0,wx.ALL,10)
        b = wx.Button(self,-1,"Go")
        b.Bind(wx.EVT_BUTTON,self.Go)
        sizer.Add(b,0,wx.ALL,10)
        self.SetSizer(sizer)
    
    def Go(self,e):
        style = 0
        if self.sortChoices.GetValue():
            style |= IP_SORT_CHOICES
        if self.sortSelected.GetValue():
            style |= IP_SORT_SELECTED
        if self.removeFromChoices.GetValue():
            style |= IP_REMOVE_FROM_CHOICES
        d = ItemsPickerDialog(self, style, self.log)
        d.ShowModal()
        
        
class ItemsPickerDialog(wx.Dialog):
    def __init__(self,parent, style, log):
        wx.Dialog.__init__(self,parent)
        self.log = log
        sizer =wx.BoxSizer(wx.VERTICAL)
        b = wx.Button(self, -1, "Add Item")
        b.Bind(wx.EVT_BUTTON, self.OnAdd)
        sizer.Add(b, 0, wx.ALL, 5)
        self.ip = ItemsPicker(self,-1, 
                          ['ThisIsItem3','ThisIsItem2','ThisIsItem1'],
                          'Stuff:', 'Selected stuff:',ipStyle = style)
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)
        self.ip._source.SetMinSize((-1,150))
        sizer.Add(self.ip, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.itemCount = 3
        self.Fit()
            
    def OnAdd(self,e):
        items = self.ip.GetItems()
        self.itemCount += 1
        newItem = "item%d" % self.itemCount
        self.ip.SetItems(items + [newItem])
        
    def OnSelectionChange(self, e):
        self.log.write("EVT_IP_SELECTION_CHANGED %s\n" % \
                        ",".join(e.GetItems()))

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>ItemsPicker </center></h2> 
    
ItemsPicker is a widget that allows the user to choose a set of picked
items out of a given list

</body></html>
"""
        

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

