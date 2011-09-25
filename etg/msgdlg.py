#---------------------------------------------------------------------------
# Name:        etg/msgdlg.py
# Author:      Kevin Ollivier
#
# Created:     24-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "msgdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  =    [
                'wxMessageDialog',
            ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMessageDialog')
    
    # These argument types are actually ButtonLabel, but the class is a private
    # helper. We will always be passing in strings, and ButtonLabel will implicitly
    # convert.
    
    c.find('SetHelpLabel.help').type = 'wxString'
    c.find('SetOKCancelLabels.ok').type = 'wxString'
    c.find('SetOKCancelLabels.cancel').type = 'wxString'
    
    c.find('SetOKLabel.ok').type = 'wxString'
    
    c.find('SetYesNoCancelLabels.yes').type = 'wxString'
    c.find('SetYesNoCancelLabels.no').type = 'wxString'
    c.find('SetYesNoCancelLabels.cancel').type = 'wxString'
    
    c.find('SetYesNoLabels.yes').type = 'wxString'
    c.find('SetYesNoLabels.no').type = 'wxString'
    
    assert isinstance(c, etgtools.ClassDef)
    
    #c.find('wxMessageDialog.title').default = 'wxEmptyString'
    #c.find('Create.title').default = 'wxEmptyString'
        
    tools.fixTopLevelWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

