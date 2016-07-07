#---------------------------------------------------------------------------
# Name:        etg/ribbon_art.py
# Author:      Robin Dunn
#
# Created:     20-Jun-2016
# Copyright:   (c) 2016 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_ribbon"
NAME      = "ribbon_art"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxRibbonArtProvider',
           'wxRibbonMSWArtProvider',
           'wxRibbonAUIArtProvider',
           ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxRibbonArtProvider')
    assert isinstance(c, etgtools.ClassDef)
    c.find('Clone').factory = True

    m = c.find('GetColourScheme')
    etgtools.appendText(m.detailedDoc, ".. seealso:: :meth:`PyGetColourScheme`")

    c.addPyMethod('PyGetColourScheme', '(self)',
        doc="""\
            A more Python friendly version of :meth:`GetColourScheme`.\n
            This method returns a tuple of the 3 colours instead of requiring
            that you provide three :class:`wx.Colour` objects to be filled in
            by the API.
            """,
        body="""\
            primary = wx.Colour()
            secondary = wx.Colour()
            tertiary = wx.Colour()
            self.GetColourScheme(primary, secondary, tertiary)
            return (primary, secondary, tertiary)
            """)


    c = module.find('wxRibbonMSWArtProvider')
    c.find('Clone').factory = True


    c = module.find('wxRibbonAUIArtProvider')
    c.find('Clone').factory = True


    module.addPyCode("""\
        if 'wxMSW' in wx.PlatformInfo:
            RibbonDefaultArtProvider = RibbonMSWArtProvider
        else:
            RibbonDefaultArtProvider = RibbonAUIArtProvider
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

