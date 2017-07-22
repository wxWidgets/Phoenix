
    # Register editor class - needs only to be called once
    multiButtonEditor = SampleMultiButtonEditor()
    wx.propgrid.PropertyGrid.RegisterEditorClass(multiButtonEditor)

    # Insert the property that will have multiple buttons
    propGrid.Append(
        wx.propgrid.LongStringProperty("MultipleButtons", wx.propgrid.PG_LABEL))

    # Change property to use editor created in the previous code segment
    propGrid.SetPropertyEditor("MultipleButtons", multiButtonEditor)

