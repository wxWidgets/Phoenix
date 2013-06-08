#---------------------------------------------------------------------------
# Name:        etg/richtextctrl.py
# Author:      Robin Dunn
#
# Created:     13-May-2013
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_richtext"
NAME      = "richtextctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxRichTextContextMenuPropertiesInfo",
           "wxRichTextCtrl",
           "wxRichTextEvent",
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxRichTextContextMenuPropertiesInfo')
    assert isinstance(c, etgtools.ClassDef)
    tools.ignoreConstOverloads(c)



    #-----------------------------------------------------------------
    c = module.find('wxRichTextCtrl')
    tools.fixWindowClass(c)
    c.bases = ['wxControl']  # wxTextctrlIface, wxScrollHelper are also bases...
    c.find('GetSelection').findOverload('from').ignore()
    tools.ignoreConstOverloads(c)

    c.find('PositionToXY.x').out = True
    c.find('PositionToXY.y').out = True
    
    c.find('HitTest.pos').out = True
    c.find('HitTest.col').out = True
    c.find('HitTest.row').out = True
    c.find('HitTest').renameOverload('row', 'HitTestXY')


    # Make sure that all the methods from wxTextEntry are included. This is
    # needed because we are pretending that this class only derives from
    # wxControl but the real C++ class also derives from wxTextCtrlIface
    # which derives from wxTextEntryBase.
    import textentry
    mod = textentry.parseAndTweakModule()
    klass = mod.find('wxTextEntry')
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             not c.findItem(item.name)]    
    c.items.extend(items)

    # TODO: What about the wxScrollHelper base class

    
    #-----------------------------------------------------------------
    c = module.find('wxRichTextEvent')
    tools.fixEventClass(c)

    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

