#---------------------------------------------------------------------------
# Name:        etg/propgridadvprops.py
# Author:      Robin Dunn
#
# Created:     25-Aug-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgridadvprops"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxColourPropertyValue',
           'wxFontProperty',
           'wxSystemColourProperty',
           'wxColourProperty',
           'wxCursorProperty',
           'wxImageFileProperty',
           'wxMultiChoiceProperty',
           'wxDateProperty',
           'wxPGSpinCtrlEditor',

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFontProperty')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixDialogProperty(c)

    c = module.find('wxMultiChoiceProperty')
    tools.fixDialogProperty(c)

    # Fix up the ctor taking a wxArrayString to be the one with the easier and
    # expected API
    m = c.find('wxMultiChoiceProperty').findOverload('strings')
    m.find('name').default = 'wxPG_LABEL'
    m.find('strings').default = 'wxArrayString()'
    m.find('strings').name = 'choices'
    m.find('value').default = 'wxArrayString()'


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')

    # Switch all StringToValue and IntToValue methods to return the variant
    # value instead of using it as a parameter.
    for item in module.allItems():
        if (item.name in ['StringToValue', 'IntToValue'] and item.findItem('variant')):
            item.find('variant').out = True


    # Deprecated aliases for the various helper classes in Classic
    module.addPyCode("""\
        PyArrayStringProperty = wx.deprecated(ArrayStringProperty, "Use ArrayStringProperty instead.")
        PyChoiceEditor = wx.deprecated(PGChoiceEditor, "Use PGChoiceEditor instead.")
        PyColourProperty = wx.deprecated(ColourProperty, "Use ColourProperty instead.")
        PyComboBoxEditor = wx.deprecated(PGComboBoxEditor, "Use PGComboBoxEditor instead.")
        PyEditEnumProperty = wx.deprecated(EditEnumProperty, "Use PGEditEnumProperty instead.")
        PyEditor = wx.deprecated(PGEditor, "Use PGEditor instead.")
        PyEditorDialogAdapter = wx.deprecated(PGEditorDialogAdapter, "Use PGEditorDialogAdapter instead.")
        PyEnumProperty = wx.deprecated(EnumProperty, "Use EnumProperty instead.")
        PyFileProperty = wx.deprecated(FileProperty, "Use FileProperty instead.")
        PyFlagsProperty = wx.deprecated(FlagsProperty, "Use FlagsProperty instead.")
        PyFloatProperty = wx.deprecated(FloatProperty, "Use FloatProperty instead.")
        PyFontProperty = wx.deprecated(FontProperty, "Use FontProperty instead.")
        PyIntProperty = wx.deprecated(IntProperty, "Use IntProperty instead.")
        PyLongStringProperty = wx.deprecated(LongStringProperty, "Use LongStringProperty instead.")
        PyProperty = wx.deprecated(PGProperty, "Use PGProperty instead.")
        PyStringProperty = wx.deprecated(StringProperty, "Use StringProperty instead.")
        PySystemColourProperty = wx.deprecated(SystemColourProperty, "Use SystemColourProperty instead.")
        PyTextCtrlEditor = wx.deprecated(PGTextCtrlEditor, "Use PGTextCtrlEditor instead.")
        PyUIntProperty = wx.deprecated(UIntProperty, "Use UIntProperty instead.")
        """)

    module.addPyFunction('RegisterEditor', '(editor, editorName)',
        deprecated='Use PropertyGrid.DoRegisterEditor instead',
        body='return PropertyGrid.DoRegisterEditorClass(editor, editorName)',
        )


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

