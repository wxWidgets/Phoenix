#---------------------------------------------------------------------------
# Name:        etg/_ribbon.py
# Author:      Robin Dunn
#
# Created:     20-Jun-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_ribbon"
NAME      = "_ribbon"   # Base name of the file to generate to for this script
DOCSTRING = """\
The `wx.ribbon` module contains a set of classes for writing a ribbon-based user interface.

At the most generic level, this is a combination of a tab control with a
toolbar. At a more functional level, it is similar to the user interface
present in recent versions of Microsoft Office and in Windows 10.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "ribbon" library in a multi-lib build.
INCLUDES = [ 'ribbon_control',
             'ribbon_page',
             'ribbon_panel',
             'ribbon_bar',
             'ribbon_art',
             'ribbon_buttonbar',
             'ribbon_gallery',
             'ribbon_toolbar',
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
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest = False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode("import wx", order=10)


    module.addInclude(INCLUDES)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

