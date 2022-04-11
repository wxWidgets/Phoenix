.. include:: headings.inc


.. _grid overview:

=================================================
|phoenix_title|  **Grid Overview**
=================================================


:class:`~wx.grid.Grid` and its related classes are used for displaying
and editing tabular data.

:class:`~wx.grid.Grid` supports custom attributes for the table cells,
allowing to completely customize its appearance and uses a separate
grid table (:class:`~wx.grid.GridTableBase` -derived) class for the
data management meaning that it can be used to display arbitrary
amounts of data.


.. _grid getting started:

Getting Started
---------------

For simple applications you need only refer to the
:class:`~wx.grid.Grid` class in your code.  This example shows how you
might create a grid in a frame or dialog constructor and illustrates
some of the formatting functions::

    import wx
    import wx.grid

    class GridFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent)

            # Create a wxGrid object
            grid = wx.grid.Grid(self, -1)

            # Then we call CreateGrid to set the dimensions of the grid
            # (100 rows and 10 columns in this example)
            grid.CreateGrid(100, 10)

            # We can set the sizes of individual rows and columns
            # in pixels
            grid.SetRowSize(0, 60)
            grid.SetColSize(0, 120)

            # And set grid cell contents as strings
            grid.SetCellValue(0, 0, 'wxGrid is good')

            # We can specify that some cells are read.only
            grid.SetCellValue(0, 3, 'This is read.only')
            grid.SetReadOnly(0, 3)

            # Colours can be specified for grid cell contents
            grid.SetCellValue(3, 3, 'green on grey')
            grid.SetCellTextColour(3, 3, wx.GREEN)
            grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

            # We can specify the some cells will store numeric
            # values rather than strings. Here we set grid column 5
            # to hold floating point values displayed with width of 6
            # and precision of 2
            grid.SetColFormatFloat(5, 6, 2)
            grid.SetCellValue(0, 6, '3.1415')

            self.Show()


    if __name__ == '__main__':

        app = wx.App(0)
        frame = GridFrame(None)
        app.MainLoop()


Here is a list of classes related to :class:`~wx.grid.Grid`:

- :class:`~wx.grid.Grid`: The main grid control class itself.
- :class:`~wx.grid.GridTableBase`: The base class for grid data provider.
- :class:`~wx.grid.GridStringTable`: Simple :class:`~wx.grid.GridTableBase` implementation
  supporting only string data items and storing them all in memory (hence suitable
  for not too large grids only).
- :class:`~wx.grid.GridCellAttr`: A cell attribute, allowing to customize its appearance
  as well as the renderer and editor used for displaying and editing it.
- :class:`~wx.grid.GridCellAttrProvider`: The object responsible for storing and retrieving the cell attributes.
- :class:`~wx.grid.GridColLabelWindow`: The window showing the grid columns labels.
- :class:`~wx.grid.GridRowLabelWindow`: The window showing the grid rows labels.
- :class:`~wx.grid.GridCornerLabelWindow`: The window used in the upper left grid corner.
- :class:`~wx.grid.GridWindow`: The window representing the main part of the grid.
- :class:`~wx.grid.GridCellRenderer`: Base class for objects used to display a cell value.
- :class:`~wx.grid.GridCellStringRenderer`: Renderer showing the cell as a text string.
- :class:`~wx.grid.GridCellNumberRenderer`: Renderer showing the cell as an integer number.
- :class:`~wx.grid.GridCellFloatRenderer`: Renderer showing the cell as a floating point number.
- :class:`~wx.grid.GridCellBoolRenderer`: Renderer showing the cell as checked or unchecked box.
- :class:`~wx.grid.GridCellEditor`: Base class for objects used to edit the cell value.
- :class:`~wx.grid.GridCellStringEditor`: Editor for cells containing text strings.
- :class:`~wx.grid.GridCellNumberEditor`: Editor for cells containing integer numbers.
- :class:`~wx.grid.GridCellFloatEditor`: Editor for cells containing floating point numbers.
- :class:`~wx.grid.GridCellBoolEditor`: Editor for boolean-valued cells.
- :class:`~wx.grid.GridCellChoiceEditor`: Editor allowing to choose one of the predefined strings (and possibly enter new one).
- :class:`~wx.grid.GridEvent`: The event sent by most of :class:`~wx.grid.Grid` actions.
- :class:`~wx.grid.GridSizeEvent`: The special event sent when a grid column or row is resized.
- :class:`~wx.grid.GridRangeSelectEvent`: The special event sent when a range of cells is selected in the grid.
- :class:`~wx.grid.GridEditorCreatedEvent`: The special event sent when a cell editor is created.
- :class:`~wx.grid.GridSelection`: The object efficiently representing the grid selection.
- :class:`~wx.grid.GridTypeRegistry`: Contains information about the data types supported by the grid.



.. _grid column and row sizes:

Column and Row Sizes
--------------------

.. note::

   This section will discuss the resizing of :class:`~wx.grid.Grid` rows
   only to avoid repetitions but everything in it also applies to grid
   columns, just replace Row in the method names with Col.


Initially all :class:`~wx.grid.Grid` rows have the same height, which
can be modified for all of them at once using
:meth:`~wx.grid.Grid.SetDefaultRowSize`. However, unlike simpler
controls such as :class:`wx.ListBox` or :class:`wx.ListCtrl`,
:class:`~wx.grid.Grid` also allows its rows to be individually resized
to have their own height using :meth:`~wx.grid.Grid.SetRowSize` (as a
special case, a row may be hidden entirely by setting its size to 0,
which is done by a helper :meth:`~wx.grid.Grid.HideRow` method). It is
also possible to resize a row to fit its contents with
:meth:`~wx.grid.Grid.AutoSizeRow` or do it for all rows at once with
:meth:`~wx.grid.Grid.AutoSizeRows`.

Additionally, by default the user can also drag the row separator
lines to resize the rows interactively.  This can be forbidden
completely by calling :meth:`~wx.grid.Grid.DisableDragRowSize` or just
for the individual rows using :meth:`~wx.grid.Grid.DisableRowResize`.

If you do allow the user to resize the grid rows, it may be a good
idea to save their heights and restore it when the grid is recreated
the next time (possibly during a next program execution): the
functions :meth:`~wx.grid.Grid.GetRowSizes` and
:meth:`~wx.grid.Grid.SetRowSizes` can help with this, you will just
need to serialize :class:`~wx.grid.GridSizesInfo` structure returned
by the former in some way and deserialize it back before calling the
latter.