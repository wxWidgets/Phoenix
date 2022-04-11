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

The following sized controls exist:

:class:`SizedFrame`
:class:`SizedDialog`
:class:`SizedPanel`
:class:`SizedScrolledPanel`
:class `SizedStaticBox`

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
        This extends the default wx.Window behavior to also add the child
        to its parent's sizer, if one exists, and set default properties.
        When an entire UI layout is managed via Sizers, this helps reduce
        the amount of sizer boilerplate code that needs to be written.

        :param `child`: child (window or another sizer) to be added to sizer.
        :type `child`: :class:`wx.Window` or :class:`wx.Sizer`
        """

        sizer = self.GetSizer()
        if sizer:
            # Note: The wx.LogNull is used here to suppress a log message
            # on wxMSW that happens because when AddChild is called the
            # widget's hwnd hasn't been set yet, so the GetWindowRect that
            # happens as a result of sizer.Add (in wxSizerItem::SetWindow)
            # fails.  A better fix would be to defer this code somehow
            # until after the child widget is fully constructed.
            nolog = wx.LogNull()
            item = sizer.Add(child)
            del nolog
            item.SetUserData({"HGrow": 0, "VGrow": 0})

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
         "form", and "grid";
        :param dict `options`: dictionary of options depending on type.

        """

        sizer = None
        self.sizerType = type
        if type == "horizontal":
            sizer = wx.BoxSizer(wx.HORIZONTAL)

        elif type == "vertical":
            sizer = wx.BoxSizer(wx.VERTICAL)

        elif type == "form":
            sizer = wx.FlexGridSizer(0, 2, 0, 0)
            #sizer.AddGrowableCol(1)

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
                sizer.AddGrowableRow(row, proportion)

            if 'growable_col' in options:
                col, proportion = options['growable_col']
                sizer.AddGrowableCol(col, proportion)

            if 'hgap' in options:
                sizer.SetHGap(options['hgap'])

            if 'vgap' in options:
                sizer.SetVGap(options['vgap'])
        if sizer:
            self._SetNewSizer(sizer)

    def _DetachFromSizer(self, sizer):
        """
        Detach children from sizer.

        :param wx.Sizer `sizer`: sizer to detach children from
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
        `self` in the following sample is a :class:`wx.SizedPanel` instance.

        Sample usage::

            self.SetSizerType("horizontal")

            b1 = wx.Button(self, wx.ID_ANY)
            t1 = wx.TextCtrl(self, -1)
            t1.SetSizerProps(expand=True)

        """

        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
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
        `self` in the following sample is a :class:`wx.SizedScrolledPanel` instance.

        Sample usage::

            self.SetSizerType("horizontal")

            b1 = wx.Button(self, wx.ID_ANY)
            t1 = wx.TextCtrl(self, -1)
            t1.SetSizerProps(expand=True)

        """

        sp.ScrolledPanel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
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
        `self` in the following sample is a :class:`wx.SizedDialog` instance.

        Sample usage::

            pane = self.GetContentsPane()
            pane.SetSizerType("horizontal")

            b1 = wx.Button(pane, wx.ID_ANY)
            t1 = wx.TextCtrl(pane, wx.ID_ANY)
            t1.SetSizerProps(expand=True)

        """

        wx.Dialog.__init__(self, *args, **kwargs)

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
        cancel = self.FindWindow(wx.ID_CANCEL)
        no = self.FindWindow(wx.ID_NO)
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
        `self` in the following sample is a :class:`wx.SizedFrame` instance

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


class SizedStaticBox(wx.StaticBox, SizedParent):
    def __init__(self, *args, **kwargs):
        wx.StaticBox.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.sizerType = "vertical"

    def AddChild(self, child):
        """
        Called automatically by wx, do not call it from user code.
        """
        wx.StaticBox.AddChild(self, child)
        SizedParent.AddChild(self, child)

    def _SetNewSizer(self, sizer):
        """
        Set a new sizer, detach old sizer, add new one and add items
        to new sizer.
        """
        props = self._DetachFromSizer(sizer)
        wx.StaticBox.SetSizer(self, sizer)
        self._AddToNewSizer(sizer, props)
