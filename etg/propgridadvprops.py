#---------------------------------------------------------------------------
# Name:        etg/propgridadvprops.py
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

    c = module.find('wxMultiChoiceProperty')
    assert isinstance(c, etgtools.ClassDef)

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

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

