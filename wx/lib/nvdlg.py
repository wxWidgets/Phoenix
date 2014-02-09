#----------------------------------------------------------------------
# Name:        wx.lib.nvdlg
# Purpose:     Dialog for editing name/value pairs
#
# Author:      Robin Dunn
#
# Created:     30-Nov-2009
# Copyright:   (c) 2009 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port
#----------------------------------------------------------------------


"""
A simple dialog that can prompt for values for any arbitrary set of name/value
pairs, where the fields are defined by a list of info passed to the
constructor. A dictionary of initial values can also be passed. Each item in
the fields list is a tuple of 3 items, which are:

    * a string to be used for the attribute name for storing the value
    * a string to be used for the label
    * None, or a dictionary of kwargs to be passed to the wx.TextCtrl ctor
"""

import wx

MARGIN = 4

    
    
class SimpleNameValueDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
                 fields=[], initialValues=None,
                 captionTitle="", captionDescr=""):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self._fields = dict()
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self._contentSizer = wx.FlexGridSizer(cols=2, hgap=MARGIN, vgap=MARGIN)
        self._contentSizer.AddGrowableCol(1)
        
        if captionTitle:
            titleTxt = wx.StaticText(self, -1, captionTitle)
            titleTxt.SetFont(wx.FFont(18, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))
            self.Sizer.Add(titleTxt, 0, wx.ALL, MARGIN)
        if captionDescr:
            descTxt = wx.StaticText(self, -1, captionDescr)
            self.Sizer.Add(descTxt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, MARGIN)
        if captionTitle or captionDescr:
            self.Sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, MARGIN)
                
        self.createFields(fields)
        self.loadValues(initialValues)
        
        self.Sizer.Add(self._contentSizer, 1, wx.EXPAND|wx.ALL, MARGIN)
        self.Sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, MARGIN)
        
        # TODO: add ability to specify which stock or custom buttons are used
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(wx.Button(self, wx.ID_OK))
        btnSizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        btnSizer.Realize()
        self.Sizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, MARGIN)
        self.FindWindowById(wx.ID_OK).SetDefault()

        self.Fit()
                
        
    def createFields(self, fields):
        self.destroyFields()
        for name, label, args in fields:
            kwargs = dict(validator=_TransferValidator(name))
            if args:
                kwargs.update(args)
            stxt = wx.StaticText(self, -1, label)
            txt = wx.TextCtrl(self, **kwargs)
            
            self._contentSizer.Add(stxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
            self._contentSizer.Add(txt, 0, wx.EXPAND)
            
            self.__dict__[name] = ""
            self._fields[name] = (stxt, txt)
            
        
    def destroyFields(self):
        for name, widgets in self._fields.iteritems():
            for w in widgets:
                w.Destroy()
            del self.__dict__[name]
            
    
    def loadValues(self, values):
        self.clearValues()
        for name, value in values.iteritems():
            if name in self._fields.keys():
                setattr(self, name, value)
    
    def clearValues(self):
        for name in self._fields.keys():
            setattr(self, name, "")

    
    
class _TransferValidator(wx.PyValidator):
    """
    This validator is used to transfer values to/from the widgets and
    attributes of the dialog.
    """
    def __init__(self, name):
        wx.PyValidator.__init__(self)
        self.name = name

    def Clone(self):
        return _TransferValidator(self.name)
    
        
    def Validate(self, win):
        return True
    
    def TransferFromWindow(self):
        dlg = self.Window.Parent
        value = dlg._fields[self.name][1].GetValue()
        setattr(dlg, self.name, value)
        return True
    
    def TransferToWindow(self):
        dlg = self.Window.Parent
        value = getattr(dlg, self.name)
        dlg._fields[self.name][1].SetValue(value)
        return True


        
        
if __name__ == '__main__':
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(redirect=False)
    #app = wx.App(redirect=False)
    
    fields = [ ('username', 'Login ID:', None),
               ('passwd',   'Password:', dict(size=(150,-1), style=wx.TE_PASSWORD)),
               ]
    
    dlg = SimpleNameValueDialog(None, title="This is the title", 
                                fields=fields, 
                                initialValues=dict(username='rdunn'),
                                captionTitle="Login",
                                captionDescr="Enter your testing credentials")
    if dlg.ShowModal() == wx.ID_OK:
        print(dlg.username, dlg.passwd)
    dlg.Destroy()
    app.MainLoop()
    
    
