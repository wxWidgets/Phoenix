#---------------------------------------------------------------------------
# Name:        etg/sizer.py
# Author:      Kevin Ollivier
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "sizer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [  'wxBoxSizer',
            'wxFlexGridSizer',
            'wxGridSizer',
            'wxSizer',
            'wxSizerFlags',
            'wxSizerItem', 
            'wxStdDialogButtonSizer',
        ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    c = module.find('wxSizer')
    for func in c.findAll('Add') + c.findAll('Insert') + c.findAll('Prepend'):
        sizer = func.findItem('sizer')
        if sizer:
            sizer.transfer = True
    c.find('GetChildren').overloads = []
    
    # Needs wxWin 2.6 compatibility to run
    c.find('Remove').findOverload('(wxWindow *window)').ignore()

    c = module.find('wxSizerItem')
    
    gud = c.find('GetUserData')
    gud.type = 'wxPyUserData*'
    gud.setCppCode('sipRes = dynamic_cast<wxPyUserData*>(sipCpp->GetUserData());')
    sud = c.find('SetUserData')
    sud.find('userData').transfer = True
    sud.find('userData').type = 'wxPyUserData*'
    sud.setCppCode('sipCpp->SetUserData(dynamic_cast<wxObject*>(userData));')

    c.addPrivateCopyCtor()

    c = module.find('wxFlexGridSizer')
    c.addPrivateCopyCtor()
    
    c = module.find('wxStdDialogButtonSizer')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()
    
    module.addPyCode("PySizer = Sizer")
        
    module.addItem(tools.wxListWrapperTemplate('wxSizerItemList', 'wxSizerItem'))
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

