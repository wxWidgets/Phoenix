#---------------------------------------------------------------------------
# Name:        etg/platinfo.py
# Author:      Robin Dunn
#
# Created:     22-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "platinfo"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPlatformInfo',
           'wxLinuxDistributionInfo',
           'wxPlatformId',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxPlatformInfo')
    assert isinstance(c, etgtools.ClassDef)

    # to avoid conflicts with wxPython's wx.PlatformInfo
    c.renameClass('PlatformInformation')

    c.find('GetEndianness').findOverload('end').ignore()
    c.find('GetArchName').findOverload('arch').ignore()
    c.find('GetOperatingSystemId').findOverload('name').ignore()
    c.find('GetPortId').findOverload('portname').ignore()
    c.find('GetEndiannessName').findOverload('end').ignore()
    c.find('GetOperatingSystemIdName').findOverload('os').ignore()
    c.find('GetOperatingSystemFamilyName').findOverload('os').ignore()
    c.find('GetPortIdName').findOverload('port').ignore()
    c.find('GetPortIdShortName').findOverload('port').ignore()
    c.find('GetBitness').findOverload('bitness').ignore()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

