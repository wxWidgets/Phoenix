#---------------------------------------------------------------------------
# Name:        etg/_propgrid.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "_propgrid"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "propgrid" library in a multi-lib build.
INCLUDES = [ 'pgvariant',
             'propgriddefs',
             'propgridproperty',
             'propgrideditors',
             'propgridpagestate',
             'propgridiface',
             'propgrid',
             'propgridprops',
             'propgridadvprops',
             'propgridmanager',
             ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [  ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode("import wx", order=10)

    module.addHeaderCode('#include <wx/propgrid/propgrid.h>')

    #module.addItem(etgtools.DefineDef(name='wxPG_INVALID_VALUE', value='INT_MAX'))

    module.addInclude(INCLUDES)

    module.addInitializerCode("""\
        wxPGInitResourceModule();
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
