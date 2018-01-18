##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to override OnCompareItems for wx.TreeCtrl.
# The overridden method simply compares lowercase item texts

def OnCompareItems(self, item1, item2):
    """Changes the sort order of the items in the tree control. """

    t1 = self.GetItemText(item1)
    t2 = self.GetItemText(item2)

    return cmp(t1.lower(), t2.lower())
