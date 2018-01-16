
    # append category
    my_cat_id = thePropGrid.Append(wx.propgrid.PropertyCategory("My Category"))

    ...

    # insert into category - using second variant
    my_item_id1 = thePropGrid.Insert(my_cat_id, 0, wx.propgrid.StringProperty("My String 1"))

    # insert before to first item - using first variant
    my_item_id2 = thePropGrid.Insert(my_item_id, wx.propgrid.StringProperty("My String 2"))
