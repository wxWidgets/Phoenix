#---------------------------------------------------------------------------
# Name:        etg/image.py
# Author:      Kevin Ollivier
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "image"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxImage', 'wxImageHistogram' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxImage')
    c.find('wxImage').findOverload('(const char *const *xpmData)').ignore()
    c.find('GetHandlers').ignore()

    # TODO: Port the ctors and methods that deal with data buffers for getting
    # and setting the image and alpha data.
    
    # TODO: Add these later when return types are defined.
    c.find('RGBtoHSV').ignore()
    c.find('HSVtoRGB').ignore()
    
    def setParamsPyInt(name):
        """Set the pyInt flag on 'unsigned char' params"""
        method = c.find(name)
        for m in [method] + method.overloads:
            for p in m.items:
                if p.type == 'unsigned char':
                    p.pyInt = True
                
    setParamsPyInt('Replace')
    setParamsPyInt('ConvertAlphaToMask')
    setParamsPyInt('ConvertToMono')
    setParamsPyInt('ConvertToDisabled')
    setParamsPyInt('IsTransparent')
    setParamsPyInt('SetAlpha')
    setParamsPyInt('SetMaskColour')
    setParamsPyInt('SetMaskFromImage')
    setParamsPyInt('SetRGB')

    
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True
    
    c.find('GetAlpha').findOverload('int x, int y').pyInt = True
    c.find('GetRed').pyInt = True
    c.find('GetGreen').pyInt = True
    c.find('GetBlue').pyInt = True
    c.find('GetMaskRed').pyInt = True
    c.find('GetMaskGreen').pyInt = True
    c.find('GetMaskBlue').pyInt = True
    
    c.find('GetOrFindMaskColour.r').pyInt = True
    c.find('GetOrFindMaskColour.g').pyInt = True
    c.find('GetOrFindMaskColour.b').pyInt = True
    c.find('GetOrFindMaskColour.r').out = True
    c.find('GetOrFindMaskColour.g').out = True
    c.find('GetOrFindMaskColour.b').out = True
    
        
    c = module.find('wxImageHistogram')
    setParamsPyInt('MakeKey')
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True
    

    module.find('wxIMAGE_ALPHA_TRANSPARENT').pyInt = True
    module.find('wxIMAGE_ALPHA_OPAQUE').pyInt = True
    
    # These are defines for string objects, not integers, so we can't generate
    # code for them the same way as integer values. Since they are #defines we
    # can't just tell SIP that they are global wxString objects because it will
    # then end up taking the address of temporary values when it makes the
    # getters for them. So instead we'll just make some python code to add the
    # .py module and hope that the interface file always has the correct
    # values of these options.
    pycode = ""
    for item in module:
        if 'IMAGE_OPTION' in item.name and isinstance(item, etgtools.DefineDef):
            item.ignore()
            name = tools.removeWxPrefix(item.name)
            value = item.value
            for txt in ['wxString(', 'wxT(', ')']:
                value = value.replace(txt, '')
                
            pycode += '%s = %s\n' % (name, value)
    module.addPyCode(pycode)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

