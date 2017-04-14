#---------------------------------------------------------------------------
# Name:        etg/utils.py
# Author:      Robin Dunn
#
# Created:     19-Dec-2010
# Copyright:   (c) 2010-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "utils"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'utils_8h.xml',
           'wxWindowDisabler',
           'wxBusyCursor',
           'wxVersionInfo',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/utils.h>')
    module.addHeaderCode('#include <wx/power.h>')


    c = module.find('wxWindowDisabler')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    # add context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'pass')


    module.find('wxQsort').ignore()
    module.find('wxGetEmailAddress').findOverload('buf').ignore()
    module.find('wxGetHostName').findOverload('buf').ignore()
    module.find('wxGetUserId').findOverload('buf').ignore()
    module.find('wxGetUserName').findOverload('buf').ignore()
    module.find('wxSortCallback').ignore()

    module.find('wxLoadUserResource').findOverload('pLen').ignore()
    module.find('wxLoadUserResource').findOverload('outData').ignore()

    module.find('wxGetFreeMemory').ignore()
    module.find('wxGetLinuxDistributionInfo').ignore()
    module.find('wxGetDisplayName').ignore()
    module.find('wxSetDisplayName').ignore()
    module.find('wxPostDelete').ignore()

    # ignore all the environment related functions
    for item in module.allItems():
        if 'Env' in item.name:
            item.ignore()
    module.find('wxGetenv').ignore()

    # Keep just the first wxExecute overload
    f = module.find('wxExecute')
    f.overloads = []
    f.mustHaveApp()

    module.find('wxGetOsVersion.major').out = True
    module.find('wxGetOsVersion.minor').out = True

    c = module.find('wxBusyCursor')
    c.mustHaveApp()
    # add context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'pass')


    for funcname in ['wxBell',
                     'wxBeginBusyCursor',
                     'wxEndBusyCursor',
                     'wxShutdown',
                     'wxInfoMessageBox',
                     'wxIsBusy',
                     'wxGetMousePosition',
                     'wxGetKeyState',
                     'wxGetMouseState',
                     ]:
        c = module.find(funcname)
        c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

