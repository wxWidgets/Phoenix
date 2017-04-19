+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| Sizer Flag                                                             | Description                                                                 |
+========================================================================+=============================================================================+
| | ``wx.TOP``                                                           | These flags are used to specify which side(s) of the sizer                  |
| | ``wx.BOTTOM``                                                        | item the border width will apply to.                                        |
| | ``wx.LEFT``                                                          |                                                                             |
| | ``wx.RIGHT``                                                         |                                                                             |
| | ``wx.ALL``                                                           |                                                                             |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``wx.EXPAND``                                                          | The item will be expanded to fill the space assigned to                     |
|                                                                        | the item.                                                                   |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``wx.SHAPED``                                                          | The item will be expanded as much as possible while also                    |
|                                                                        | maintaining its aspect ratio                                                |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``wx.FIXED_MINSIZE``                                                   | Normally `wx.Sizers` will use                                               |
|                                                                        | :meth:`wx.Window.GetEffectiveMinSize` to                                    |
|                                                                        | determine what the minimal size of window items should be, and will use that|
|                                                                        | size to calculate the layout. This allows layouts to adjust when an item    |
|                                                                        | changes and its best size becomes different. If you would rather have a     |
|                                                                        | window item stay the size it started with then use ``wx.FIXED_MINSIZE``.    |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``wx.RESERVE_SPACE_EVEN_IF_HIDDEN``                                    | Normally `wx.Sizers` don't allocate space for hidden windows or other items.|
|                                                                        | This flag overrides this behavior so that sufficient space is allocated for |
|                                                                        | the window even if it isn't visible. This makes it possible to dynamically  |
|                                                                        | show and hide controls without resizing parent dialog, for example.         |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| | ``wx.ALIGN_CENTER`` **or** ``wx.ALIGN_CENTRE``                       | The ``wx.ALIGN*`` flags allow you to specify the alignment of the item      |
| | ``wx.ALIGN_LEFT``                                                    | within the space allotted to it by the sizer, adjusted for the border if    |
| | ``wx.ALIGN_RIGHT``                                                   | any.                                                                        |
| | ``wx.ALIGN_RIGHT``                                                   |                                                                             |
| | ``wx.ALIGN_TOP``                                                     |                                                                             |
| | ``wx.ALIGN_BOTTOM``                                                  |                                                                             |
| | ``wx.ALIGN_CENTER_VERTICAL`` **or** ``wx.ALIGN_CENTRE_VERTICAL``     |                                                                             |
| | ``wx.ALIGN_CENTER_HORIZONTAL`` **or** ``wx.ALIGN_CENTRE_HORIZONTAL`` |                                                                             |
+------------------------------------------------------------------------+-----------------------------------------------------------------------------+

|

