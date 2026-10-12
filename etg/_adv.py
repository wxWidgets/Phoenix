#---------------------------------------------------------------------------
# Name:        etg/_adv.py
# Author:      Robin Dunn
#
# Created:     22-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "_adv"   # Base name of the file to generate to for this script
DOCSTRING = """\
The ``wx.adv`` module contains classes which are more advanced and/or less
commonly used than those in the core namespace. They are provided in a
separate module to help reduce overhead and dependencies for those
applications which do not need any of these classes.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "adv" library in a multi-lib build.
INCLUDES = [
             'aboutdlg',
             'helpext',
             'commandlinkbutton',
             'dateevt',
             'datectrl',
             'calctrl',
             'hyperlink',
             'tipdlg',
             'taskbar',
             'sound',
             'joystick',
             'animate',
             'bannerwindow',
             'editlbox',
             'notifmsg',
             'splash',
             'sashwin',
             'laywin',
             'odcombo',
             'bmpcbox',
             'richtooltip',
             'timectrl',
             'wizard',
             'pseudodc',
             'propdlg',
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
    module.addHeaderCode('#include <wx/help.h>')

    module.addImport('_core')
    module.addPyCode("import wx", order=10)
    module.addInclude(INCLUDES)


    # Redo the initialization of wxModules in the case where this extension
    # module is not imported until *after* the wx.App has been created.
    module.addInitializerCode("""\
        wxPyReinitializeModules();
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
