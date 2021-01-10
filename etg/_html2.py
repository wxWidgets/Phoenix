#---------------------------------------------------------------------------
# Name:        etg/_html2.py
# Author:      Robin Dunn
#
# Created:     20-Nov-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools


PACKAGE   = "wx"
MODULE    = "_html2"
NAME      = "_html2"   # Base name of the file to generate to for this script
DOCSTRING = """\
The ``wx.html2`` module includes a widget class and supporting classes that
wraps native browser components on the system, therefore providing a fully
featured HTML rendering component including the latest HTML, Javascript and
CSS standards. Since platform-specific back-ends are used (Microsoft Trident,
WebKit webView, etc.) there will be some difference in ability and behaviors,
but these classes will minimize those differences as much as possible.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "webview" library in a multi-lib build.
INCLUDES = [ 'webview',
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
    module.addPyCode('import wx', order=10)
    module.addInclude(INCLUDES)


    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
