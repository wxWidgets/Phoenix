#---------------------------------------------------------------------------
# Name:        etg/_aui.py
# Author:      Robin Dunn
#
# Created:     25-Oct-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_aui"
NAME      = "_aui"   # Base name of the file to generate to for this script
DOCSTRING = """\
`wx.aui` provides a set of classes for implementing an "Advanced User Interface".
More specifically, these classes enable to you present some of your application in
floating or dockable panels, notebooks with floatable tabs, etc.

There is also a pure-python implementation of these classes available in the
`wx.lib.agw.aui` package.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "aui" library in a multi-lib build.
INCLUDES = [ 'auiframemanager',
             'auidockart',
             'auibar',
             'auibook',
             'auitabmdi',
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

    module.addHeaderCode('#include <wx/aui/aui.h>')

    module.addInclude(INCLUDES)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
