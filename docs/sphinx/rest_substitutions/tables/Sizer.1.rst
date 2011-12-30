+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| Sizer Flag                                                          | Description                                                                 |
+=====================================================================+=============================================================================+
| ``TOP``                                                             | These flags are used to specify which side(s) of the sizer                  |
+---------------------------------------------------------------------+ item the border width will apply to.                                        | 
| ``BOTTOM``                                                          |                                                                             |
+---------------------------------------------------------------------+                                                                             |
| ``LEFT``                                                            |                                                                             |
+---------------------------------------------------------------------+                                                                             |
| ``RIGHT``                                                           |                                                                             |
+---------------------------------------------------------------------+                                                                             |
| ``ALL``                                                             |                                                                             |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``EXPAND``                                                          | The item will be expanded to fill the space assigned to                     |
|                                                                     | the item.                                                                   |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``SHAPED``                                                          | The item will be expanded as much as possible while also                    |
|                                                                     | maintaining its aspect ratio                                                |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``FIXED_MINSIZE``                                                   | Normally `Sizers` will use                                                  |
|                                                                     | :meth:`Window.GetAdjustedBestSize` to                                       |
|                                                                     | determine what the minimal size of window items should be, and will use that| 
|                                                                     | size to calculate the layout. This allows layouts to adjust when an item    |
|                                                                     | changes and its best size becomes different. If you would rather have a     |
|                                                                     | window item stay the size it started with then use ``FIXED_MINSIZE``.       |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``RESERVE_SPACE_EVEN_IF_HIDDEN``                                    | Normally `Sizers` don't allocate space for hidden windows or other items.   | 
|                                                                     | This flag overrides this behavior so that sufficient space is allocated for |
| .. versionadded:: 2.8.8                                             | the window even if it isn't visible. This makes it possible to dynamically  |
|                                                                     | show and hide controls without resizing parent dialog, for example.         |
|                                                                     | Available since version 2.8.8                                               |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+
| ``ALIGN_CENTER`` **or** ``ALIGN_CENTRE``                            | The ``ALIGN*`` flags allow you to specify the alignment of the item         |
+---------------------------------------------------------------------+ within the space allotted to it by the sizer, adjusted for the border if    |
| ``ALIGN_LEFT``                                                      | any.                                                                        |
+---------------------------------------------------------------------+                                                                             | 
| ``ALIGN_RIGHT``                                                     |                                                                             |
+---------------------------------------------------------------------+                                                                             | 
| ``ALIGN_TOP``                                                       |                                                                             |
+---------------------------------------------------------------------+                                                                             | 
| ``ALIGN_BOTTOM``                                                    |                                                                             |
+---------------------------------------------------------------------+                                                                             | 
| ``ALIGN_CENTER_VERTICAL`` **or** ``ALIGN_CENTRE_VERTICAL``          |                                                                             |
+---------------------------------------------------------------------+                                                                             | 
| ``ALIGN_CENTER_HORIZONTAL`` **or** ``ALIGN_CENTRE_HORIZONTAL``      |                                                                             |
+---------------------------------------------------------------------+-----------------------------------------------------------------------------+

|

