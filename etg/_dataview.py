#---------------------------------------------------------------------------
# Name:        etg/_dataview.py
# Author:      Kevin Ollivier
#
# Created:     12-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx" 
MODULE    = "_dataview"
NAME      = "_dataview"   # Base name of the file to generate to for this script
DOCSTRING = ""

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

INCLUDES = [
              'dataview',
              'dataviewhelpers',          
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
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode("""\
        #include <wx/wx.h>
        #include "wxpy_utils.h"
        """)
    module.addImport('_core')
    module.addInclude(INCLUDES)
    
    # This code is inserted into the module initialization function
    module.addPostInitializerCode("""
    wxPyDataViewModuleInject(sipModuleDict);
    """)
    # Here is the function it calls
    module.addCppCode(wxPyDataViewModuleInject)
                      
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

wxPyDataViewModuleInject = """
void wxPyDataViewModuleInject(PyObject* moduleDict)
{

}
"""

if __name__ == '__main__':
    run()
