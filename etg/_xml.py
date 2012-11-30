#---------------------------------------------------------------------------
# Name:        etg/_xml.py
# Author:      Robin Dunn
#
# Created:     28-Nov-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx" 
MODULE    = "_xml"
NAME      = "_xml"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxXmlNode',
           'wxXmlAttribute',
           'wxXmlDocument',
           ]    
    

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "xml" library in a multi-lib build.
INCLUDES = [ ]


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
    module.addPyCode('import wx', order=10)
    module.addInclude(INCLUDES)


    #-----------------------------------------------------------------
    
    
    module.addPyCode("""\
        XmlProperty = wx.deprecated(XmlAttribute, 'Use XmlProperty instead.')
        """)
    
    c = module.find('wxXmlNode')
    assert isinstance(c, etgtools.ClassDef)
    
    c.find('wxXmlNode.parent').transferThis = True
    
    c.find('AddAttribute.attr').transfer = True
    c.find('AddChild.child').transfer = True
    c.find('InsertChild.child').transfer = True
    c.find('InsertChildAfter.child').transfer = True
    c.find('RemoveChild.child').transferBack = True
    
    # we like the other overload better
    c.find('GetAttribute').findOverload('value').ignore()
    
    c.find('SetAttributes').ignore()
    c.find('SetChildren').ignore()
    
    
        
    c = module.find('wxXmlDocument')
    c.find('GetEncoding').ignore()
    c.find('SetEncoding').ignore()
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
