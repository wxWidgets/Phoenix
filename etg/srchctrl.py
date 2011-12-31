#---------------------------------------------------------------------------
# Name:        etg/srchctrl.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "srchctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxSearchCtrl' ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/srchctrl.h>')

    c = module.find('wxSearchCtrl')
    assert isinstance(c, etgtools.ClassDef)
    
    c.find('SetMenu.menu').transfer = True

    c.addCppMethod('void', 'SetSearchBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchBitmap(*bmp);
            #endif
            """)
    c.addCppMethod('void', 'SetSearchMenuBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchMenuBitmap(*bmp);
            #endif
            """)
    c.addCppMethod('void', 'SetCancelBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchMenuBitmap(*bmp);
            #endif
            """)

    # Not using autoProperties here because some getters use 'Is'
    c.addProperty('Menu GetMenu SetMenu')
    c.addProperty('SearchButtonVisible IsSearchButtonVisible ShowSearchButton')
    c.addProperty('CancelButtonVisible IsCancelButtonVisible ShowCancelButton')
    c.addProperty('DescriptiveText GetDescriptiveText SetDescriptiveText')

    tools.fixWindowClass(c)
    
        
    module.addPyCode("""\
        EVT_SEARCHCTRL_CANCEL_BTN = wx.PyEventBinder( wxEVT_COMMAND_SEARCHCTRL_CANCEL_BTN, 1)
        EVT_SEARCHCTRL_SEARCH_BTN = wx.PyEventBinder( wxEVT_COMMAND_SEARCHCTRL_SEARCH_BTN, 1)
        """)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

