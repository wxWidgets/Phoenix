#---------------------------------------------------------------------------
# Name:        etg/pen.py
# Author:      Robin Dunn
#
# Created:     31-Aug-2011
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "pen"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxPen' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxPen')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    c.find('GetDashes').ignore()
    c.find('SetDashes').ignore()
    c.addCppMethod('wxArrayInt*', 'GetDashes', '()', """\
                   wxArrayInt* arr = new wxArrayInt;
                   wxDash* dashes;
                   int num = self->GetDashes(&dashes);
                   for (int i=0; i<num; i++)
                       arr->Add(dashes[i]);
                    return arr;""")
    
    # TODO: SetDashes needs to keep the wxDash array alive as long as the pen
    # is alive, but the pen does not take ownership of the array... Classic
    # wxPython did some black magic here, is that still the best way?
    
    # TODO: Fix these. I'm not sure why exactly, but in the CPP code
    # they end up with the wrong signature.
    module.find('wxRED_PEN').ignore()
    module.find('wxBLUE_PEN').ignore()
    module.find('wxCYAN_PEN').ignore()
    module.find('wxGREEN_PEN').ignore()
    module.find('wxYELLOW_PEN').ignore()
    module.find('wxBLACK_PEN').ignore()
    module.find('wxWHITE_PEN').ignore()
    module.find('wxTRANSPARENT_PEN').ignore()
    module.find('wxBLACK_DASHED_PEN').ignore()
    module.find('wxGREY_PEN').ignore()
    module.find('wxMEDIUM_GREY_PEN').ignore()
    module.find('wxLIGHT_GREY_PEN').ignore()

    module.find('wxThePenList').ignore()
    #module.addItem(tools.wxListWrapperTemplate('wxBrushList', 'wxBrush'))
    #module.addItem(tools.wxListWrapperTemplate('wxPenList', 'wxPen'))

    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

