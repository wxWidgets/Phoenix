
    pgMan = wx.propgrid.PropertyGridManager(
        parent,
        PGID,
        # These and other similar styles are automatically
        # passed to the embedded wx.PropertyGrid.
        style = wx.PG_BOLD_MODIFIED|wx.PG_SPLITTER_AUTO_CENTER|
        # Include toolbar.
        wx.PG_TOOLBAR |
        # Include description box.
        wx.PG_DESCRIPTION |
        # Include compactor.
        wx.PG_COMPACTOR |
        # Plus defaults.
        wx.PGMAN_DEFAULT_STYLE
      )

    page = pgMan.AddPage("First Page")
    page.Append(wx.propgrid.PropertyCategory("Category A1"))
    page.Append(wx.propgrid.IntProperty("Number", wx.propgrid.PG_LABEL, 1))
    page.Append(wx.propgrid.ColourProperty("Colour",wx.propgrid.PG_LABEL, wx.WHITE))

    page = pgMan.AddPage("Second Page")
    page.Append("Text", wx.propgrid.PG_LABEL, "(no text)")
    page.Append(wx.propgrid.FontProperty("Font",wx.propgrid.PG_LABEL))

    # Display a header above the grid
    pgMan.ShowHeader()
