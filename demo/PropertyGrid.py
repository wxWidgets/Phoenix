#!/usr/bin/env python

import sys
import time
import math
import os.path

import wx
import wx.adv
import wx.propgrid as wxpg

from six import exec_
_ = wx.GetTranslation


############################################################################
#
# TEST RELATED CODE AND VARIABLES
#
############################################################################

default_object_content2 = """\
object.title = "Object Title"
object.index = 1
object.PI = %f
object.wxpython_rules = True
"""%(math.pi)

default_object_content1 = """\

#
# Note that the results of autofill will appear on the second page.

#
# Set number of iterations appropriately to test performance
iterations = 100

#
# Test result for 100,000 iterations on Athlon XP 2000+:
#
# Time spent per property: 0.054ms
# Memory allocated per property: ~350 bytes (includes Python object)
#

for i in range(0,iterations):
    setattr(object,'title%i'%i,"Object Title")
    setattr(object,'index%i'%i,1)
    setattr(object,'PI%i'%i,3.14)
    setattr(object,'wxpython_rules%i'%i,True)
"""


############################################################################
#
# CUSTOM PROPERTY SAMPLES
#
############################################################################


class ValueObject:
    def __init__(self):
        pass


class IntProperty2(wxpg.PGProperty):
    """
    This is a simple re-implementation of wxIntProperty.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=0):
        wxpg.PGProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        """
        If failed, return False or (False, None). If success, return tuple
        (True, newValue).
        """
        try:
            v = int(s)
            if self.GetValue() != v:
                return (True, v)
        except (ValueError, TypeError):
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number."%s, "Error")
        return (False, None)

    def IntToValue(self, v, flags):
        """
        If failed, return False or (False, None). If success, return tuple
        (True, newValue).
        """
        if (self.GetValue() != v):
            return (True, v)
        return False

    def ValidateValue(self, value, validationInfo):
        """ Let's limit the value to range -10000 and 10000.
        """
        # Just test this function to make sure validationInfo and
        # wxPGVFBFlags work properly.
        oldvfb__ = validationInfo.GetFailureBehavior()

        # Mark the cell if validation failed
        validationInfo.SetFailureBehavior(wxpg.PG_VFB_MARK_CELL)

        if value is None or value < -10000 or value > 10000:
            return False

        return True


class SizeProperty(wxpg.PGProperty):
    """ Demonstrates a property with few children.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=wx.Size(0, 0)):
        wxpg.PGProperty.__init__(self, label, name)

        value = self._ConvertValue(value)

        self.AddPrivateChild( wxpg.IntProperty("X", value=value.x) )
        self.AddPrivateChild( wxpg.IntProperty("Y", value=value.y) )

        self.m_value = value

    def GetClassName(self):
        return self.__class__.__name__

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def RefreshChildren(self):
        size = self.m_value
        self.Item(0).SetValue( size.x )
        self.Item(1).SetValue( size.y )

    def _ConvertValue(self, value):
        """ Utility convert arbitrary value to a real wx.Size.
        """
        import collections
        if isinstance(value, collections.Sequence) or hasattr(value, '__getitem__'):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, thisValue, childIndex, childValue):
        size = self._ConvertValue(self.m_value)
        if childIndex == 0:
            size.x = childValue
        elif childIndex == 1:
            size.y = childValue
        else:
            raise AssertionError

        return size


class DirsProperty(wxpg.ArrayStringProperty):
    """ Sample of a custom custom ArrayStringProperty.

        Because currently some of the C++ helpers from wxArrayStringProperty
        and wxProperytGrid are not available, our implementation has to quite
        a bit 'manually'. Which is not too bad since Python has excellent
        string and list manipulation facilities.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=[]):
        wxpg.ArrayStringProperty.__init__(self, label, name, value)
        self.m_display = ''
        # Set default delimiter
        self.SetAttribute("Delimiter", ',')


    # NOTE: In the Classic version of the propgrid classes, all of the wrapped
    # property classes override DoGetEditorClass so it calls GetEditor and
    # looks up the class using that name, and hides DoGetEditorClass from the
    # usable API. Jumping through those hoops is no longer needed in Phoenix
    # as Phoenix allows overriding all necessary virtual methods without
    # special support in the wrapper code, so we just need to override
    # DoGetEditorClass here instead.
    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")


    def ValueToString(self, value, flags):
        # let's just use the cached display value
        return self.m_display


    def OnSetValue(self):
        self.GenerateValueAsString()


    def DoSetAttribute(self, name, value):
        retval = super(DirsProperty, self).DoSetAttribute(name, value)

        # Must re-generate cached string when delimiter changes
        if name == "Delimiter":
            self.GenerateValueAsString(delim=value)

        return retval


    def GenerateValueAsString(self, delim=None):
        """ This function creates a cached version of displayed text
            (self.m_display).
        """
        if not delim:
            delim = self.GetAttribute("Delimiter")
            if not delim:
                delim = ','

        ls = self.GetValue()
        if delim == '"' or delim == "'":
            text = ' '.join(['%s%s%s'%(delim,a,delim) for a in ls])
        else:
            text = ', '.join(ls)
        self.m_display = text


    def StringToValue(self, text, argFlags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        delim = self.GetAttribute("Delimiter")
        if delim == '"' or delim == "'":
            # Proper way to call same method from super class
            return super(DirsProperty, self).StringToValue(text, 0)
        v = [a.strip() for a in text.split(delim)]
        return (True, v)


    def OnEvent(self, propgrid, primaryEditor, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            dlg = wx.DirDialog(propgrid,
                               _("Select a directory to be added to "
                                 "the list:"))

            if dlg.ShowModal() == wx.ID_OK:
                new_path = dlg.GetPath()
                old_value = self.m_value
                if old_value:
                    new_value = list(old_value)
                    new_value.append(new_path)
                else:
                    new_value = [new_path]
                self.SetValueInEvent(new_value)
                retval = True
            else:
                retval = False

            dlg.Destroy()
            return retval

        return False



class PyObjectPropertyValue:
    """
    Value type of our sample PyObjectProperty. We keep a simple dash-delimited
    list of string given as argument to constructor.
    """
    def __init__(self, s=None):
        try:
            self.ls = [a.strip() for a in s.split('-')]
        except:
            self.ls = []

    def __repr__(self):
        return ' - '.join(self.ls)


class PyObjectProperty(wxpg.PGProperty):
    """
    Another simple example. This time our value is a PyObject.

    NOTE: We can't return an arbitrary python object in DoGetValue. It cannot
          be a simple type such as int, bool, double, or string, nor an array
          or wxObject based. Dictionary, None, or any user-specified Python
          class is allowed.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=None):
        wxpg.PGProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return repr(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        v = PyObjectPropertyValue(s)
        return (True, v)


class SampleMultiButtonEditor(wxpg.PGTextCtrlEditor):
    def __init__(self):
        wxpg.PGTextCtrlEditor.__init__(self)

    def CreateControls(self, propGrid, property, pos, sz):
        # Create and populate buttons-subwindow
        buttons = wxpg.PGMultiButton(propGrid, sz)

        # Add two regular buttons
        buttons.AddButton("...")
        buttons.AddButton("A")
        # Add a bitmap button
        buttons.AddBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FOLDER))

        # Create the 'primary' editor control (textctrl in this case)
        wnd = super(SampleMultiButtonEditor, self).CreateControls(
                                   propGrid,
                                   property,
                                   pos,
                                   buttons.GetPrimarySize())
        wnd = wnd.GetPrimary()

        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(propGrid, pos);

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.buttons = buttons

        return wxpg.PGWindowList(wnd, buttons)

    def OnEvent(self, propGrid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            evtId = event.GetId()

            if evtId == buttons.GetButtonId(0):
                # Do something when the first button is pressed
                wx.LogDebug("First button pressed")
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # Do something when the second button is pressed
                wx.MessageBox("Second button pressed")
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(2):
                # Do something when the third button is pressed
                wx.MessageBox("Third button pressed")
                return False  # Return false since value did not change

        return super(SampleMultiButtonEditor, self).OnEvent(propGrid, prop, ctrl, event)


class SingleChoiceDialogAdapter(wxpg.PGEditorDialogAdapter):
    """ This demonstrates use of wxpg.PGEditorDialogAdapter.
    """
    def __init__(self, choices):
        wxpg.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        s = wx.GetSingleChoice("Message", "Caption", self.choices)

        if s:
            self.SetValue(s)
            return True

        return False;


class SingleChoiceProperty(wxpg.StringProperty):
    def __init__(self, label, name=wxpg.PG_LABEL, value=''):
        wxpg.StringProperty.__init__(self, label, name, value)

        # Prepare choices
        dialog_choices = []
        dialog_choices.append("Cat")
        dialog_choices.append("Dog")
        dialog_choices.append("Gibbon")
        dialog_choices.append("Otter")

        self.dialog_choices = dialog_choices

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")

    def GetEditorDialog(self):
        # Set what happens on button click
        return SingleChoiceDialogAdapter(self.dialog_choices)


class TrivialPropertyEditor(wxpg.PGEditor):
    """
    This is a simple re-creation of TextCtrlWithButton. Note that it does
    not take advantage of wx.TextCtrl and wx.Button creation helper functions
    in wx.PropertyGrid.
    """
    def __init__(self):
        wxpg.PGEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        """ Create the actual wxPython controls here for editing the
            property value.

            You must use propgrid.GetPanel() as parent for created controls.

            Return value is either single editor control or tuple of two
            editor controls, of which first is the primary one and second
            is usually a button.
        """
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString();

            tc = wx.TextCtrl(propgrid.GetPanel(), wx.ID_ANY, s,
                             (x,y), (w,h),
                             wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wx.ID_ANY, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)
            return wxpg.PGWindowList(tc, btn)
        except:
            import traceback
            print(traceback.print_exc())

    def UpdateControl(self, property, ctrl):
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired successfully.
        """
        tc = ctrl
        textVal = tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (True, None)

        res, value = property.StringToValue(textVal, wxpg.PG_FULL_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        ctrl.Remove(0,len(ctrl.GetValue()))

    def SetControlStringValue(self, property, ctrl, text):
        ctrl.SetValue(text)

    def OnFocus(self, property, ctrl):
        ctrl.SetSelection(-1,-1)



class LargeImageEditor(wxpg.PGEditor):
    """
    Double-height text-editor with image in front.
    """
    def __init__(self):
        wxpg.PGEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            self.property = property

            self.RefreshThumbnail()
            self.statbmp = wx.StaticBitmap(propgrid.GetPanel(), -1, self.bmp, (x,y))
            self.tc = wx.TextCtrl(propgrid.GetPanel(), -1,  "",
                                  (x+h,y), (2048,h), wx.BORDER_NONE)

            btn = wx.Button(propgrid.GetPanel(), wx.ID_ANY, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)

            # When the textctrl is destroyed, destroy the statbmp too
            def _cleanupStatBmp(evt):
                if self.statbmp:
                    self.statbmp.Destroy()
            self.tc.Bind(wx.EVT_WINDOW_DESTROY, _cleanupStatBmp)

            return wxpg.PGWindowList(self.tc, btn)
        except:
            import traceback
            print(traceback.print_exc())


    def GetName(self):
        return "LargeImageEditor"


    def UpdateControl(self, property, ctrl):
        s = property.GetDisplayedString()
        self.tc.SetValue(s)
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)


    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired successfully.
        """
        textVal = self.tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (None, True)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)


    def SetValueToUnspecified(self, property, ctrl):
        ctrl.Remove(0, len(ctrl.GetValue()))
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def SetControlStringValue(self, property, ctrl, txt):
        self.tc.SetValue(txt)
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def CanContainCustomImage(self):
        return True


    def RefreshThumbnail(self):
        """
        We use here very simple image scaling code.
        """
        def _makeEmptyBmp():
            bmp = wx.Bitmap(64,64)
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(0, 0, 64, 64)
            return bmp

        if not self.property:
            self.bmp = _makeEmptyBmp()
            return

        path = self.property.DoGetValue()

        if not os.path.isfile(path):
            self.bmp = _makeEmptyBmp()
            return

        image = wx.Image(path)
        image.Rescale(64, 64)
        self.bmp = wx.Bitmap(image)


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################

class TestPanel( wx.Panel ):

    def __init__( self, parent, log ):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.log = log

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )


        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        if not getattr(sys, '_PropGridEditorsRegistered', False):
            pg.RegisterEditor(TrivialPropertyEditor)
            pg.RegisterEditor(SampleMultiButtonEditor)
            pg.RegisterEditor(LargeImageEditor)
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #
        # NOTE: in this example the property names are used as variable names
        # in one of the tests, so they need to be valid python identifiers.
        #
        pg.AddPage( "Page 1 - Testing All" )

        pg.Append( wxpg.PropertyCategory("1 - Basic Properties") )
        pg.Append( wxpg.StringProperty("String",value="Some Text") )

        sp = pg.Append( wxpg.StringProperty('StringProperty_as_Password', value='ABadPassword') )
        sp.SetAttribute('Hint', 'This is a hint')
        sp.SetAttribute('Password', True)

        pg.Append( wxpg.IntProperty("Int", value=100) )
        self.fprop = pg.Append( wxpg.FloatProperty("Float", value=123.456) )
        pg.Append( wxpg.BoolProperty("Bool", value=True) )
        boolprop = pg.Append( wxpg.BoolProperty("Bool_with_Checkbox", value=True) )
        pg.SetPropertyAttribute(
            "Bool_with_Checkbox",    # You can find the property by name,
            #boolprop,               # or give the property object itself.
            "UseCheckbox", True)     # The attribute name and value

        pg.Append( wxpg.PropertyCategory("2 - More Properties") )
        pg.Append( wxpg.LongStringProperty("LongString",
            value="This is a\nmulti-line string\nwith\ttabs\nmixed\tin."))
        pg.Append( wxpg.DirProperty("Dir",value=r"C:\Windows") )
        pg.Append( wxpg.FileProperty("File",value=r"C:\Windows\system.ini") )
        pg.Append( wxpg.ArrayStringProperty("ArrayString",value=['A','B','C']) )

        pg.Append( wxpg.EnumProperty("Enum","Enum",
                                     ['wxPython Rules',
                                      'wxPython Rocks',
                                      'wxPython Is The Best'],
                                     [10,11,12],
                                     0) )
        pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
                                         ['A','B','C'],
                                         [0,1,2],
                                         "Text Not in List") )

        pg.Append( wxpg.PropertyCategory("3 - Advanced Properties") )
        pg.Append( wxpg.DateProperty("Date",value=wx.DateTime.Now()) )
        pg.Append( wxpg.FontProperty("Font",value=panel.GetFont()) )
        pg.Append( wxpg.ColourProperty("Colour",
                                       value=panel.GetBackgroundColour()) )
        pg.Append( wxpg.SystemColourProperty("SystemColour") )
        pg.Append( wxpg.ImageFileProperty("ImageFile") )
        pg.Append( wxpg.MultiChoiceProperty("MultiChoice",
                    choices=['wxWidgets','QT','GTK+']) )

        pg.Append( wxpg.PropertyCategory("4 - Additional Properties") )
        #pg.Append( wxpg.PointProperty("Point",value=panel.GetPosition()) )
        pg.Append( SizeProperty("Size", value=panel.GetSize()) )
        #pg.Append( wxpg.FontDataProperty("FontData") )
        pg.Append( wxpg.IntProperty("IntWithSpin",value=256) )
        pg.SetPropertyEditor("IntWithSpin","SpinCtrl")

        pg.SetPropertyAttribute( "File", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
        pg.SetPropertyAttribute( "File", wxpg.PG_FILE_INITIAL_PATH,
                                 r"C:\Program Files\Internet Explorer" )
        pg.SetPropertyAttribute( "Date", wxpg.PG_DATE_PICKER_STYLE,
                                 wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY )

        pg.Append( wxpg.PropertyCategory("5 - Custom Properties and Editors") )
        pg.Append( IntProperty2("IntProperty2", value=1024) )

        pg.Append( PyObjectProperty("PyObjectProperty") )

        pg.Append( DirsProperty("Dirs1",value=['C:/Lib','C:/Bin']) )
        pg.Append( DirsProperty("Dirs2",value=['/lib','/bin']) )

        # Test another type of delimiter
        pg.SetPropertyAttribute("Dirs2", "Delimiter", '"')

        # SampleMultiButtonEditor
        pg.Append( wxpg.LongStringProperty("MultipleButtons") )
        pg.SetPropertyEditor("MultipleButtons", "SampleMultiButtonEditor")
        pg.Append( SingleChoiceProperty("SingleChoiceProperty") )

        # Custom editor samples
        prop = pg.Append( wxpg.StringProperty("StringWithCustomEditor",
                                              value="test value") )
        pg.SetPropertyEditor(prop, "TrivialPropertyEditor")

        pg.Append( wxpg.ImageFileProperty("ImageFileWithLargeEditor") )
        pg.SetPropertyEditor("ImageFileWithLargeEditor", "LargeImageEditor")

        # When page is added, it will become the target page for AutoFill
        # calls (and for other property insertion methods as well)
        pg.AddPage( "Page 2 - Results of AutoFill will appear here" )

        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"SetPropertyValues")
        but.Bind( wx.EVT_BUTTON, self.OnSetPropertyValues )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"GetPropertyValues")
        but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"GetPropertyValues(as_strings=True)")
        but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues2 )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"AutoFill")
        but.Bind( wx.EVT_BUTTON, self.OnAutoFill )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"Delete")
        but.Bind( wx.EVT_BUTTON, self.OnDeleteProperty )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"Run Tests")
        but.Bind( wx.EVT_BUTTON, self.RunTests )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s changed to "%s"\n' % (p.GetName(),p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s selected\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing selected\n')

    def OnDeleteProperty(self, event):
        p = self.pg.GetSelectedProperty()
        if p:
            self.pg.DeleteProperty(p)
        else:
            wx.MessageBox("First select a property to delete")

    def OnReserved(self, event):
        pass

    def OnSetPropertyValues(self,event):
        try:
            d = self.pg.GetPropertyValues(inc_attributes=True)

            ss = []
            for k,v in d.items():
                v = repr(v)
                if not v or v[0] != '<':
                    if k.startswith('@'):
                        ss.append('setattr(obj, "%s", %s)'%(k,v))
                    else:
                        ss.append('obj.%s = %s'%(k,v))

            with MemoDialog(self,
                    "Enter Content for Object Used in SetPropertyValues",
                    '\n'.join(ss)) as dlg:  # default_object_content1

                if dlg.ShowModal() == wx.ID_OK:
                    import datetime
                    sandbox = {'obj':ValueObject(),
                               'wx':wx,
                               'datetime':datetime}
                    exec_(dlg.tc.GetValue(), sandbox)
                    t_start = time.time()
                    #print(sandbox['obj'].__dict__)
                    self.pg.SetPropertyValues(sandbox['obj'])
                    t_end = time.time()
                    self.log.write('SetPropertyValues finished in %.0fms\n' %
                                   ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(inc_attributes=True)
            t_end = time.time()
            self.log.write('GetPropertyValues finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.items()]
            with MemoDialog(self,"GetPropertyValues Result",
                           'Contents of resulting dictionary:\n\n'+'\n'.join(ss)) as dlg:
                dlg.ShowModal()

        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues2(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(as_strings=True)
            t_end = time.time()
            self.log.write('GetPropertyValues(as_strings=True) finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.items()]
            with MemoDialog(self,"GetPropertyValues Result",
                           'Contents of resulting dictionary:\n\n'+'\n'.join(ss)) as dlg:
                dlg.ShowModal()
        except:
            import traceback
            traceback.print_exc()

    def OnAutoFill(self,event):
        try:
            with MemoDialog(self,"Enter Content for Object Used for AutoFill",default_object_content1) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    sandbox = {'object':ValueObject(),'wx':wx}
                    exec_(dlg.tc.GetValue(), sandbox)
                    t_start = time.time()
                    self.pg.AutoFill(sandbox['object'])
                    t_end = time.time()
                    self.log.write('AutoFill finished in %.0fms\n' %
                                   ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s right clicked\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing right clicked\n')

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()
        self.log.write('Page Changed to \'%s\'\n' % (self.pg.GetPageName(index)))

    def RunTests(self, event):
        pg = self.pg
        log = self.log

        # Validate client data
        log.write('Testing client data set/get')
        pg.SetPropertyClientData( "Bool", 1234 )
        if pg.GetPropertyClientData( "Bool" ) != 1234:
            raise ValueError("Set/GetPropertyClientData() failed")

        # Test setting unicode string
        log.write('Testing setting an unicode string value')
        pg.GetPropertyByName("String").SetValue(u"Some Unicode Text")

        #
        # Test some code that *should* fail (but not crash)
        try:
            if wx.GetApp().GetAssertionMode() == wx.PYAPP_ASSERT_EXCEPTION:
                log.write('Testing exception handling compliancy')
                a_ = pg.GetPropertyValue( "NotARealProperty" )
                pg.EnableProperty( "NotAtAllRealProperty", False )
                pg.SetPropertyHelpString("AgaintNotARealProperty",
                                         "Dummy Help String" )
        except:
            pass

        # GetPyIterator
        log.write('GetPage(0).GetPyIterator()\n')
        it = pg.GetPage(0).GetPyIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # VIterator
        log.write('GetPyVIterator()\n')
        it = pg.GetPyVIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Properties
        log.write('GetPage(0).Properties\n')
        it = pg.GetPage(0).Properties
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Items
        log.write('GetPage(0).Items\n')
        it = pg.GetPage(0).Items
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

#---------------------------------------------------------------------------


class MemoDialog(wx.Dialog):
    """
    Dialog for multi-line text editing.
    """
    def __init__(self,parent=None,title="",text="",pos=None,size=(500,500)):
        wx.Dialog.__init__(self,parent,-1,title,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer( wx.VERTICAL )

        tc = wx.TextCtrl(self,11,text,style=wx.TE_MULTILINE)
        self.tc = tc
        topsizer.Add(tc,1,wx.EXPAND|wx.ALL,8)

        rowsizer = wx.BoxSizer( wx.HORIZONTAL )
        rowsizer.Add(wx.Button(self,wx.ID_OK,'Ok'),0,wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add((0,0),1,wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'),0,wx.ALIGN_CENTRE_VERTICAL,8)
        topsizer.Add(rowsizer,0,wx.EXPAND|wx.ALL,8)

        self.SetSizer( topsizer )
        topsizer.Layout()

        self.SetSize( size )
        if not pos:
            self.CenterOnScreen()
        else:
            self.Move(pos)

#----------------------------------------------------------------------

def runTest( frame, nb, log ):
    win = TestPanel( nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
This demo shows all basic wxPropertyGrid properties, in addition to
some custom property classes.
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

