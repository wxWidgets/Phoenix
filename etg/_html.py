#---------------------------------------------------------------------------
# Name:        etg/_html.py
# Author:      Robin Dunn
#
# Created:     27-Oct-2012
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx" 
MODULE    = "_html"
NAME      = "_html"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ ]    
    

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "html" library in a multi-lib build.
INCLUDES = [  
             'htmldefs',
             'htmlcell',
             'htmlfilt',
             'htmltag',
             'htmlpars',
             'htmlwin',
             'htmlprint',
             'htmlwinpars',
             
             'helpdata',
             'helpfrm',
             'helpdlg',
             'helpwnd',
             'helpctrl',
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
    
    module.addHeaderCode('#include <wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode("import wx", order=10)
    module.addInclude(INCLUDES)
       
    module.addCppCode("""\
        #include <wx/html/htmlwin.h>
        #include <wx/html/htmprint.h>
        #include <wx/html/helpctrl.h>
        #include <wx/html/helpwnd.h>
        #include <wx/html/helpfrm.h>
        #include <wx/html/helpdlg.h>
        """)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
