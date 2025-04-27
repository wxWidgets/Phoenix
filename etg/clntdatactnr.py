#---------------------------------------------------------------------------
# Name:        etg/clntdatactnr.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "clntdatactnr"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxClientDataContainer',
           'wxSharedClientDataContainer' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxClientDataContainer')
    assert isinstance(c, etgtools.ClassDef)


    # The [G|S]etClientData methods deal with untyped void* values, which we
    # don't support. The [G|S]etClientObject methods use wxClientData instances
    # which we have a MappedType for, so make the ClientData methods just be
    # aliases for ClientObjects. From the Python programmer's perspective they
    # would be virtually the same anyway.
    c.find('SetClientObject.data').transfer = True
    c.find('GetClientData').ignore()
    c.find('SetClientData').ignore()
    c.find('GetClientObject').pyName = 'GetClientData'
    c.find('SetClientObject').pyName = 'SetClientData'
    c.addPyMethod('GetClientObject', '(self)',
        doc="Alias for :meth:`GetClientData`",
        body="return self.GetClientData()")
    c.addPyMethod('SetClientObject', '(self, data)',
        doc="Alias for :meth:`SetClientData`",
        body="self.SetClientData(data)")
    c.addPyProperty('ClientData GetClientData SetClientData')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

