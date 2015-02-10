#----------------------------------------------------------------------
# Name:        sized_controls.py
# Purpose:     Implements default, HIG-compliant sizers under the hood
#              and provides a simple interface for customizing those sizers.
#
# Author:      Kevin Ollivier
#
# Created:     26-May-2006
# Copyright:   (c) 2006 Kevin Ollivier
# Licence:     wxWindows license
#
#
# Tags:        phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------
"""
The sized controls default HIG compliant sizers under the hood and provides
a simple interface for customizing those sizers.

The following sized controls exists:

:class:`SizedFrame`
:class:`SizedDialog`
:class:`SizedPanel`
:class:`SizedScrolledPanel`

Description
===========

The sized controls allow you to create sizer based layouts without having to
code the sizers by hand, but still provide you the manual detailed control of
the sizer and sizer items if necessary.

Usage
=====

Sample usage::

    import wx
    import wx.lib.sized_controls as sc

    app = wx.App(0)

    frame = sc.SizedFrame(None, -1, "A sized frame")
    
    pane = frame.GetContentsPane()
    pane.SetSizerType("horizontal")
    
    b1 = wx.Button(pane, wx.ID_ANY)
    t1 = wx.TextCtrl(pane, -1)
    t1.SetSizerProps(expand=True)

    frame.Show()

    app.MainLoop()

"""

import wx
import wx.lib.scrolledpanel as sp

# For HIG info: links to all the HIGs can be found here: 
# http://en.wikipedia.org/wiki/Human_Interface_Guidelines


# useful defines for sizer prop values

halign = {  "left": wx.ALIGN_LEFT,
            "center": wx.ALIGN_CENTER_HORIZONTAL,
            "centre": wx.ALIGN_CENTRE_HORIZONTAL,
            "right": wx.ALIGN_RIGHT,
         }
        
valign = {  "top": wx.ALIGN_TOP,
            "bottom": wx.ALIGN_BOTTOM,
            "center": wx.ALIGN_CENTER_VERTICAL,
            "centre": wx.ALIGN_CENTRE_VERTICAL,
         }
         
align = {   "center": wx.ALIGN_CENTER,
            "centre": wx.ALIGN_CENTRE, 
        }
        
border = {  "left": wx.LEFT,
            "right": wx.RIGHT,
            "top": wx.TOP,
            "bottom": wx.BOTTOM,
            "all": wx.ALL,
         }
           
minsize = {   "fixed":    wx.FIXED_MINSIZE,
          }
                
misc_flags = {   "expand": wx.EXPAND, }


class TableSizer(wx.Sizer):
    """
    An attempt at creating a more intuitive replacement for nesting box sizers.
    """
    def __init__(self, rows=0, cols=0):
        wx.Sizer.__init__(self)
        self.rows = rows
        self.cols = cols
        self.fixed_width = 0
        self.fixed_height = 0
        self.hgrow = 0
        self.vgrow = 0
        
        self.row_widths = []
        self.col_heights = []
        
        # allow us to use 'old-style' proportions when emulating box sizers
        self.isHorizontal = (self.rows == 1 and self.cols == 0)
        self.isVertical = (self.cols == 1 and self.rows == 0)
        
    def CalcNumRowsCols(self):
        """
        Calculate the number of rows and columns needed.

        :returns: The number of rows and columns needed by the sizer.
        :rtype: `tuple`
        """
        numrows = self.rows
        numcols = self.cols
        numchild = len(self.GetChildren())
        
        if numrows == 0 and numcols == 0:
            return 0, 0
        
        if numrows == 0:
            rows, mod = divmod(numchild, self.cols)
            if mod > 0:
                rows += 1
            numrows = rows
            
        if numcols == 0:
            cols, mod = divmod(numchild, self.rows)
            if mod > 0:
                cols += 1
            numcols = cols
            
        return numrows, numcols
        
    def CalcMin(self):
        """
        Calculate the minimum size.
        
        :rtype: :ref:`Size`
        
        """
        numrows, numcols = self.CalcNumRowsCols() 
        numchild = len(self.GetChildren())
        
        if numchild == 0:
            return wx.Size(10, 10)
            
        if numrows == 0 and numcols == 0:
            print("TableSizer must have the number of rows or columns set. Cannot continue.")
            return wx.Size(10, 10)
       
        self.row_widths = [0 for x in range(0, numrows)]
        self.col_heights = [0 for x in range(0, numcols)]
        currentRow = 0
        currentCol = 0
        counter = 0
        self.hgrow = 0
        self.vgrow = 0

        # get the max row width and max column height
        for item in self.GetChildren():            
            if self.cols != 0:
                currentRow, currentCol = divmod(counter, numcols)
            else:
                currentCol, currentRow = divmod(counter, numrows)
            
            if item.IsShown():
                width, height = item.CalcMin()
                
                if self.isVertical and item.GetProportion() > 0:
                    self.hgrow += item.GetProportion()
                elif self.isHorizontal and item.GetProportion() > 0:
                    self.vgrow += item.GetProportion()
                
                if width > self.row_widths[currentRow]:
                    self.row_widths[currentRow] = width
                
                if height > self.col_heights[currentCol]:
                    self.col_heights[currentCol] = height
            
            counter += 1
                
        minwidth = 0
        for row_width in self.row_widths:
            minwidth += row_width
            
        minheight = 0
        for col_height in self.col_heights:
            minheight += col_height
                
        self.fixed_width = minwidth
        self.fixed_height = minheight
        
        return wx.Size(minwidth, minheight)
        
    def RecalcSizes(self):
        """
        Recalculate the sizes.
        """
        
        numrows, numcols = self.CalcNumRowsCols()
        numchild = len(self.GetChildren())
        
        if numchild == 0:
            return
        currentRow = 0
        currentCol = 0
        counter = 0
        
        print("cols %d, rows %d" % (self.cols, self.rows))
        print("fixed_height %d, fixed_width %d" % (self.fixed_height, self.fixed_width))
        #print("self.GetSize() = " + `self.GetSize()`)
        
        row_widths = [0 for x in range(0, numrows)]
        col_heights = [0 for x in range(0, numcols)]
        item_sizes = [0 for x in range(0, len(self.GetChildren()))]
        grow_sizes = [0 for x in range(0, len(self.GetChildren()))]
        
        curHPos = 0
        curVPos = 0
        curCol = 0
        curRow = 0
        # first, we set sizes for all children, and while doing so, calc
        # the maximum row heights and col widths. Then, afterwards we handle
        # the positioning of the controls                
        
        for item in self.GetChildren():
            if self.cols != 0:
                currentRow, currentCol = divmod(counter, numcols)
            else:
                currentCol, currentRow = divmod(counter, numrows)
            if item.IsShown():
                item_minsize = item.GetMinSizeWithBorder()
                width = item_minsize[0]
                height = item_minsize[1]
                
                print("row_height %d, row_width %d" % (self.col_heights[currentCol], self.row_widths[currentRow]))
                growable_width = (self.GetSize()[0]) - width
                growable_height = (self.GetSize()[1]) - height
                
                #if not self.isVertical and not self.isHorizontal:
                #    growable_width = self.GetSize()[0] - self.row_widths[currentRow]
                #    growable_height = self.GetSize()[1] - self.col_heights[currentCol]
                
                #print("grow_height %d, grow_width %d" % (growable_height, growable_width))
                
                item_vgrow = 0
                item_hgrow = 0
                # support wx.EXPAND for box sizers to be compatible
                if item.GetFlag() & wx.EXPAND:
                    if self.isVertical:
                        if self.hgrow > 0 and item.GetProportion() > 0:
                            item_hgrow = (growable_width * item.GetProportion()) / self.hgrow
                        item_vgrow = growable_height 

                    elif self.isHorizontal: 
                        if self.vgrow > 0 and item.GetProportion() > 0:
                            item_vgrow = (growable_height * item.GetProportion()) / self.vgrow
                        item_hgrow = growable_width
                        
                if growable_width > 0 and item.GetHGrow() > 0:
                    item_hgrow = (growable_width * item.GetHGrow()) / 100
                    print("hgrow = %d" % (item_hgrow))

                if growable_height > 0 and item.GetVGrow() > 0:
                    item_vgrow = (growable_height * item.GetVGrow()) / 100
                    print("vgrow = %d" % (item_vgrow))
                
                grow_size = wx.Size(item_hgrow, item_vgrow)
                size = item_minsize #wx.Size(item_minsize[0] + item_hgrow, item_minsize[1] + item_vgrow) 
                if size[0] + grow_size[0] > row_widths[currentRow]:
                    row_widths[currentRow] = size[0] + grow_size[0]
                if size[1] + grow_size[1] > col_heights[currentCol]:
                    col_heights[currentCol] = size[1] + grow_size[1] 
                
                grow_sizes[counter] = grow_size
                item_sizes[counter] = size
            
            counter += 1
        
        counter = 0
        for item in self.GetChildren():
            if self.cols != 0:
                currentRow, currentCol = divmod(counter, numcols)
            else:
                currentCol, currentRow = divmod(counter, numrows)
            
            itempos = self.GetPosition()
            if item.IsShown():
                rowstart = itempos[0] 
                for row in range(0, currentRow):
                    rowstart += row_widths[row]
                    
                colstart = itempos[1]
                for col in range(0, currentCol):
                    #print("numcols = %d, currentCol = %d, col = %d" % (numcols, currentCol, col))
                    colstart += col_heights[col]
                    
                itempos[0] += rowstart
                itempos[1] += colstart
                
                if item.GetFlag() & wx.ALIGN_RIGHT:
                    itempos[0] += (row_widths[currentRow] - item_sizes[counter][0])
                elif item.GetFlag() & (wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL):
                    itempos[0] += (row_widths[currentRow] - item_sizes[counter][0]) / 2
                
                if item.GetFlag() & wx.ALIGN_BOTTOM:
                    itempos[1] += (col_heights[currentCol] - item_sizes[counter][1])
                elif item.GetFlag() & (wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL):
                    itempos[1] += (col_heights[currentCol] - item_sizes[counter][1]) / 2
                
                hgrowth =  (grow_sizes[counter][0] - itempos[0])
                if hgrowth > 0:
                    item_sizes[counter][0] += hgrowth
                
                vgrowth =  (grow_sizes[counter][1] - itempos[1])
                if vgrowth > 0:
                    item_sizes[counter][1] += vgrowth
                #item_sizes[counter][1] -= itempos[1]
                item.SetDimension(itempos, item_sizes[counter])
                    
            counter += 1

def GetDefaultBorder(self):
    """
    Return the platform specific default border.

    :rtype: `int`
    """
    border = 4
    if wx.Platform == "__WXMAC__":
        border = 6 
    elif wx.Platform == "__WXMSW__":
        # MSW HIGs use dialog units, not pixels
        pnt = self.ConvertDialogToPixels(wx.Point(4, 4))
        border = pnt[0] // 2
    elif wx.Platform == "__WXGTK__":
        border = 3 

    return border

def SetDefaultSizerProps(self):
    """
    Set default sizer properties.
    """
    item = self.GetParent().GetSizer().GetItem(self)    
    item.SetProportion(0)
    item.SetFlag(wx.ALL)
    item.SetBorder(self.GetDefaultHIGBorder())
        
def GetSizerProps(self):
    """
    Returns a dictionary of prop name + value.
    """
    props = {}
    item = self.GetParent().GetSizer().GetItem(self)
    if item is None:
        return None
    
    props['proportion'] = item.GetProportion()
    flags = item.GetFlag()

    if flags & border['all'] == border['all']:
        props['border'] = (['all'], item.GetBorder())
    else:
        borders = []
        for key in border:
            if flags & border[key]:
                borders.append(key)      
            
        props['border'] = (borders, item.GetBorder())
    
    if flags & align['center'] == align['center']:
        props['align'] = 'center'
    else:
        for key in halign:
            if flags & halign[key]:
                props['halign'] = key

        for key in valign:
            if flags & valign[key]:
                props['valign'] = key
    
    for key in minsize:
        if flags & minsize[key]:
            props['minsize'] = key 
    
    for key in misc_flags:
        if flags & misc_flags[key]:
            props[key] = "true"
            
    return props

def SetSizerProp(self, prop, value):
    """
    Sets a sizer property
    
    Sample usages::
    
        control.SetSizerProp('expand', True)
    
    :param string `prop`: valid strings are "proportion", "hgrow", "vgrow",
     "align", "halign", "valign", "border", "minsize" and "expand"
    :param `value`: corresponding value for the prop
    """
    
    lprop = prop.lower()
    sizer = self.GetParent().GetSizer()
    item = sizer.GetItem(self) 
    flag = item.GetFlag()
    if lprop == "proportion":
        item.SetProportion(int(value))
    elif lprop == "hgrow":
        item.SetHGrow(int(value))
    elif lprop == "vgrow":
        item.SetVGrow(int(value))
    elif lprop == "align":
        flag = flag | align[value]
    elif lprop == "halign":
        flag = flag | halign[value]
    elif lprop == "valign":
        flag = flag | valign[value]
    # elif lprop == "border":
    #     # this arg takes a tuple (dir, pixels)
    #     dirs, amount = value
    #     if dirs == "all":
    #         dirs = ["all"]
    #     for dir in dirs:
    #         flag = flag | border[dir]
    #     item.SetBorder(amount)
    elif lprop == "border":
        # this arg takes a tuple (dir, pixels)
        dirs, amount = value
        if dirs == "all":
            dirs = ["all"]
        else:
            flag &= ~(wx.ALL)
        for dir in dirs:
            flag = flag | border[dir]
        item.SetBorder(amount)
    elif lprop == "minsize":
        flag = flag | minsize[value]
    elif lprop in misc_flags:
        if not value or str(value) == "" or str(value).lower() == "false":
            flag = flag &~ misc_flags[lprop]
        else:
            flag = flag | misc_flags[lprop]
    
    # auto-adjust growable rows/columns if expand or proportion is set
    # on a sizer item in a FlexGridSizer
    if lprop in ["expand", "proportion"] and isinstance(sizer, wx.FlexGridSizer):
        cols = sizer.GetCols()
        rows = sizer.GetRows()
        # FIXME: I'd like to get the item index in the sizer instead, but
        # doing sizer.GetChildren.index(item) always gives an error
        itemnum = self.GetParent().GetChildren().index(self)
                
        col = 0
        row = 0
        if cols == 0:
            col, row = divmod( itemnum, rows )
        else:
            row, col = divmod( itemnum, cols )
        
        if lprop == "expand" and not sizer.IsColGrowable(col):
            sizer.AddGrowableCol(col)
        elif lprop == "proportion" and int(value) != 0 and not sizer.IsRowGrowable(row):
            sizer.AddGrowableRow(row)

    item.SetFlag(flag)

def SetSizerProps(self, props={}, **kwargs):
    """
    Allows to set multiple sizer properties
        
    Sample usages::
    
        control.SetSizerProps(expand=True, proportion=1)
    
        control.SetSizerProps(expand=True, valign='center', border=(['top',
                                                                     'bottom'], 5))
                                                                 
        control.SetSizerProps({'growable_row': (1, 1),
                               'growable_col': (0, 1),})

    :param dict `props`: a dictionary of prop name + value
    :param `kwargs`: keywords can be used for properties, e.g. expand=True
    
    """

    allprops = {}
    allprops.update(props)
    allprops.update(kwargs)
    
    for prop in allprops:
        self.SetSizerProp(prop, allprops[prop])
        
def GetDialogBorder(self):
    """
    Get the platform specific dialog border.

    :rtype: `int`
    """
    
    border = 6
    if wx.Platform == "__WXMAC__" or wx.Platform == "__WXGTK__":
        border = 12
    elif wx.Platform == "__WXMSW__":
        pnt = self.ConvertDialogToPixels(wx.Point(7, 7))
        border = pnt[0]
    
    return border

def SetHGrow(self, proportion):
    """
    Set horizontal grow proportion.
    
    :param int `proportion`: proportion to use
    """
    
    data = self.GetUserData()
    if "HGrow" in data:
        data["HGrow"] = proportion
        self.SetUserData(data) 
    
def GetHGrow(self):
    """
    Get the horizontal grow value.

    :rtype: `int`
    """
    
    if self.GetUserData() and "HGrow" in self.GetUserData():
        return self.GetUserData()["HGrow"]
    else:
        return 0
        
def SetVGrow(self, proportion):
    """
    Set vertical grow proportion.
    
    :param int `proportion`: proportion to use
    """
    
    data = self.GetUserData()
    if "VGrow" in data:
        data["VGrow"] = proportion
        self.SetUserData(data) 
    
def GetVGrow(self):
    """
    Get the vertical grow value.

    :rtype: `int`
    """
    
    if self.GetUserData() and "VGrow" in self.GetUserData():
        return self.GetUserData()["VGrow"]
    else:
        return 0

def GetDefaultPanelBorder(self):
    """
    Default panel border is set to 0 by default as the child control
    will set their borders.
    """
    return 0

# Why, Python?! Why do you make it so easy?! ;-)    
wx.Dialog.GetDialogBorder = GetDialogBorder
wx.Panel.GetDefaultHIGBorder = GetDefaultPanelBorder
wx.Notebook.GetDefaultHIGBorder = GetDefaultPanelBorder
wx.SplitterWindow.GetDefaultHIGBorder = GetDefaultPanelBorder

wx.Window.GetDefaultHIGBorder = GetDefaultBorder
wx.Window.SetDefaultSizerProps = SetDefaultSizerProps
wx.Window.SetSizerProp = SetSizerProp
wx.Window.SetSizerProps = SetSizerProps
wx.Window.GetSizerProps = GetSizerProps

wx.SizerItem.SetHGrow = SetHGrow
wx.SizerItem.GetHGrow = GetHGrow
wx.SizerItem.SetVGrow = SetVGrow
wx.SizerItem.GetVGrow = GetVGrow


class SizedParent:
    """
    Mixin class for some methods used by the ``Sized*`` classes.
    """
    def AddChild(self, child):
        """
        Add a child to sizer
        
        :param `child`: child (window or another sizer) to be added to sizer.
        :type `child`: :class:`Window` or :class:`Sizer`
        """
        
        # Note: The wx.LogNull is used here to suppress a log message
        # on wxMSW that happens because when AddChild is called the
        # widget's hwnd hasn't been set yet, so the GetWindowRect that
        # happens as a result of sizer.Add (in wxSizerItem::SetWindow)
        # fails.  A better fix would be to defer this code somehow
        # until after the child widget is fully constructed.
        sizer = self.GetSizer()
        nolog = wx.LogNull()
        item = sizer.Add(child)
        del nolog
        item.SetUserData({"HGrow":0, "VGrow":0})
        
        # Note: One problem is that the child class given to AddChild
        # is the underlying wxWidgets control, not its Python subclass. So if 
        # you derive your own class, and override that class' GetDefaultBorder(), 
        # etc. methods, it will have no effect.  
        child.SetDefaultSizerProps()
        
    def GetSizerType(self):
        """
        Return the sizer type.

        :rtype: `string`
        """
        
        return self.sizerType
    
    def SetSizerType(self, type, options={}):
        """
        Sets the sizer type and automatically re-assign any children
        to it.
        
        :param string `type`: sizer type, valid values are "horizontal", "vertical",
         "form", "table" and "grid";
        :param dict `options`: dictionary of options depending on type.
        
        """

        sizer = None
        self.sizerType = type
        if type == "horizontal":
            sizer = wx.BoxSizer(wx.HORIZONTAL) # TableSizer(0, 1) 
        
        elif type == "vertical":
            sizer = wx.BoxSizer(wx.VERTICAL) # TableSizer(1, 0)
        
        elif type == "form":
            #sizer = TableSizer(2, 0)
            sizer = wx.FlexGridSizer(0, 2, 0, 0)
            #sizer.AddGrowableCol(1)
            
        elif type == "table":
            rows = cols = 0
            if 'rows' in options:
                rows = int(options['rows'])

            if 'cols' in options:
                cols = int(options['cols'])
        
            sizer = TableSizer(rows, cols)
        
        elif type == "grid":
            sizer = wx.FlexGridSizer(0, 0, 0, 0)
            if 'rows' in options:
                sizer.SetRows(int(options['rows']))
            else:
                sizer.SetRows(0)
            if 'cols' in options:
                sizer.SetCols(int(options['cols']))
            else:
                sizer.SetCols(0)
    
            if 'growable_row' in options:
                row, proportion = options['growable_row']
                sizer.SetGrowableRow(row, proportion)
            
            if 'growable_col' in options:
                col, proportion = options['growable_col']
                sizer.SetGrowableCol(col, proportion)
            
            if 'hgap' in options:
                sizer.SetHGap(options['hgap'])
                
            if 'vgap' in options:
                sizer.SetVGap(options['vgap'])
        if sizer:
            self._SetNewSizer(sizer)
                
    def _DetachFromSizer(self, sizer):
        """
        Detach children from sizer.
        
        :param Sizer `sizer`: sizer to detach children from
        """
        
        props = {}
        for child in self.GetChildren():
            # On the Mac the scrollbars and corner gripper of a
            # ScrolledWindow will be in the list of children, but
            # should not be managed by a sizer.  So if there is a
            # child that is not in a sizer make sure we don't track
            # info for it nor add it to the next sizer.
            csp = child.GetSizerProps()
            if csp is not None:
                props[child.GetId()] = csp
                self.GetSizer().Detach(child)

        return props

    def _AddToNewSizer(self, sizer, props):
        """
        Add children to new sizer.
        
        :param `sizer`: param is not used, remove it ???
        :param `props`: sizer properties
        
        """
        for child in self.GetChildren():
            csp = props.get(child.GetId(), None)
            # See Mac comment above.
            if csp is not None:
                self.GetSizer().Add(child)
                child.SetSizerProps(csp)


class SizedPanel(wx.Panel, SizedParent):
    """
    A sized panel.
    
    Controls added to it will automatically be added to its sizer.
    """
    def __init__(self, *args, **kwargs):
        """
        `self` in the following sample is a :class:`SizedPanel` instance.

        Sample usage::
        
            self.SetSizerType("horizontal")
        
            b1 = wx.Button(self, wx.ID_ANY)
            t1 = wx.TextCtrl(self, -1)
            t1.SetSizerProps(expand=True)
        
        """

        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL) #TableSizer(1, 0)
        self.SetSizer(sizer)
        self.sizerType = "vertical"

    def AddChild(self, child):
        """
        Called automatically by wx, do not call it from user code.
        """
        wx.Panel.AddChild(self, child)
        SizedParent.AddChild(self, child)

    def _SetNewSizer(self, sizer):
        """
        Set a new sizer, detach old sizer, add new one and add items
        to new sizer.
        """
        props = self._DetachFromSizer(sizer)
        wx.Panel.SetSizer(self, sizer)
        self._AddToNewSizer(sizer, props)


class SizedScrolledPanel(sp.ScrolledPanel, SizedParent):
    """
    A sized scrolled panel.
    
    Controls added to it will automatically be added to its sizer.
    """
    def __init__(self, *args, **kwargs):
        """
        `self` in the following sample is a :class:`SizedScrolledPanel` instance.

        Sample usage::
        
            self.SetSizerType("horizontal")
            
            b1 = wx.Button(self, wx.ID_ANY)
            t1 = wx.TextCtrl(self, -1)
            t1.SetSizerProps(expand=True)

        """

        sp.ScrolledPanel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL) #TableSizer(1, 0)
        self.SetSizer(sizer)
        self.sizerType = "vertical"
        self.SetupScrolling()

    def AddChild(self, child):
        """
        Called automatically by wx, should not be called from user code.

        :param `child`: child (window or another sizer) to be added to sizer.
        """
        sp.ScrolledPanel.AddChild(self, child)
        SizedParent.AddChild(self, child)

    def _SetNewSizer(self, sizer):
        """
        Set a new sizer, detach old sizer, add new one and add items
        to new sizer.
        """
        props = self._DetachFromSizer(sizer)
        sp.ScrolledPanel.SetSizer(self, sizer)
        self._AddToNewSizer(sizer, props)


class SizedDialog(wx.Dialog):
    """A sized dialog
    
    Controls added to its content pane will automatically be added to 
    the panes sizer.
    """
    def __init__(self, *args, **kwargs):    
        """
        `self` in the following sample is a :class:`SizedDialog` instance.

        Sample usage::
        
            pane = self.GetContentsPane()
            pane.SetSizerType("horizontal")
        
            b1 = wx.Button(pane, wx.ID_ANY)
            t1 = wx.TextCtrl(pane, wx.ID_ANY)
            t1.SetSizerProps(expand=True)
        
        """
 
        wx.Dialog.__init__(self, *args, **kwargs)
        
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        
        self.borderLen = 12
        self.mainPanel = SizedPanel(self, -1)
        
        mysizer = wx.BoxSizer(wx.VERTICAL)
        mysizer.Add(self.mainPanel, 1, wx.EXPAND | wx.ALL, self.GetDialogBorder())
        self.SetSizer(mysizer)
        
        self.SetAutoLayout(True)
        
    def GetContentsPane(self):
        """
        Return the pane to add controls too.
        """
        return self.mainPanel
        
    def SetButtonSizer(self, sizer):
        """
        Set a sizer for buttons and adjust the button order.
        """
        self.GetSizer().Add(sizer, 0, wx.EXPAND | wx.BOTTOM | wx.RIGHT, self.GetDialogBorder())
        
        # Temporary hack to fix button ordering problems.
        cancel = self.FindWindowById(wx.ID_CANCEL, parent=self)
        no = self.FindWindowById(wx.ID_NO, parent=self)
        if no and cancel:
            cancel.MoveAfterInTabOrder(no)
            
class SizedFrame(wx.Frame):
    """
    A sized frame.
        
    Controls added to its content pane will automatically be added to 
    the panes sizer.
    """
    
    def __init__(self, *args, **kwargs):    
        """
        `self` in the following sample is a :class:`SizedFrame` instance

        Sample usage::
        
            pane = self.GetContentsPane()
            pane.SetSizerType("horizontal")
            
            b1 = wx.Button(pane, wx.ID_ANY)
            t1 = wx.TextCtrl(pane, -1)
            t1.SetSizerProps(expand=True)
        
        """

        wx.Frame.__init__(self, *args, **kwargs)
        
        self.borderLen = 12
        # this probably isn't needed, but I thought it would help to make it consistent
        # with SizedDialog, and creating a panel to hold things is often good practice.
        self.mainPanel = SizedPanel(self, -1)
        
        mysizer = wx.BoxSizer(wx.VERTICAL)
        mysizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(mysizer)
        
        self.SetAutoLayout(True)
        
    def GetContentsPane(self):
        """
        Return the pane to add controls too
        """
        return self.mainPanel
