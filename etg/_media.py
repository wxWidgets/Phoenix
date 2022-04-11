#---------------------------------------------------------------------------
# Name:        etg/_media.py
# Author:      Dietmar Schwertberger
#
# Created:     13-Nov-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------


import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_media"
NAME      = "_media"   # Base name of the file to generate to for this script
DOCSTRING = """\
The ``wx.media`` module provides a widget class that allows displaying various
types of media, such as video and audio files and streaming, using native
system components.  The wxWidgets media classes are an optional part of the
build so it may not always be available on your build of wxPython.
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

INCLUDES = [  'mediactrl',
           ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [ ]


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
