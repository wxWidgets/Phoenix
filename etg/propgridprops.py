#---------------------------------------------------------------------------
# Name:        etg/propgridprops.py
# Author:      Robin Dunn
#
# Created:     25-Aug-2016
# Copyright:   (c) 2016-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgridprops"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPGInDialogValidator',
           'wxStringProperty',
           'wxNumericPropertyValidator',
           'wxIntProperty',
           'wxUIntProperty',
           'wxFloatProperty',
           'wxBoolProperty',
           'wxEnumProperty',
           'wxEditEnumProperty',
           'wxFlagsProperty',
           'wxPGFileDialogAdapter',
           'wxFileProperty',
           'wxPGLongStringDialogAdapter',
           'wxLongStringProperty',
           'wxDirProperty',
           'wxArrayStringProperty',
           'wxPGArrayEditorDialog',
           'wxPGArrayStringEditorDialog',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxNumericPropertyValidator')
    assert isinstance(c, etgtools.ClassDef)
    c.bases = ['wxValidator']


    for name in ['wxEnumProperty', 'wxEditEnumProperty']:
        c = module.find(name)
        # Ignore problematic ctors, that we don't need anyway.
        # Yes, there are two of them
        c.find(name).findOverload('wxChar').ignore()
        c.find(name).findOverload('wxChar').ignore()

        m = c.find(name).findOverload('wxArrayString')
        m.find('label').default = 'wxPG_LABEL'
        m.find('name').default = 'wxPG_LABEL'
        m.find('labels').default = 'wxArrayString()'


    c = module.find('wxFlagsProperty')
    # Ignore problematic ctors, that we don't need anyway.
    c.find('wxFlagsProperty').findOverload('wxChar').ignore()


    c = module.find('wxIntProperty')
    # clear the parts of the docstrings that are not really applicable to Python
    c.briefDoc = "Basic property with integer value."
    c.detailedDoc = []

    c = module.find('wxLongStringProperty')
    c.find('OnButtonClick.value').inOut = True
    c.find('DisplayEditorDialog.value').inOut = True

    c = module.find('wxDirProperty')
    c.find('OnButtonClick.value').inOut = True

    c = module.find('wxArrayStringProperty')
    c.find('GenerateValueAsString').ignore(False)

    c = module.find('wxPGArrayEditorDialog')
    tools.fixWindowClass(c, hideVirtuals=False, ignoreProtected=False)

    c = module.find('wxPGArrayStringEditorDialog')
    tools.fixWindowClass(c, hideVirtuals=False, ignoreProtected=False)


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

