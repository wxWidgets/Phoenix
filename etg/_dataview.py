#---------------------------------------------------------------------------
# Name:        etg/_dataview.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     12-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_dataview"
NAME      = "_dataview"   # Base name of the file to generate to for this script
DOCSTRING = """\
The classes in this module provide views and data models for viewing tabular
or hierarchical data in a more advanced way than what is provided by classes
such as :ref:`wx.ListCtrl`, :ref:`wx.TreeCtrl`, etc.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These items are in their own etg scripts
# for easier maintainability, but their class and function definitions are
# intended to be part of this module, not their own module. This also makes it
# easier to promote one of these to module status later if desired, simply
# remove it from this list of Includes, and change the MODULE value in the
# promoted script to be the same as its NAME.
INCLUDES = [ 'dvcvariant',
             'dataview',
             'treelist',
             ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from setup.py for a list of sources and a list
# of additional dependencies when building this extension module
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = []


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING, check4unittest=False)
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
