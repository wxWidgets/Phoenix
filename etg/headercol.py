#---------------------------------------------------------------------------
# Name:        etg/headercol.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "headercol"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxHeaderColumn', 'wxSettableHeaderColumn', 'wxHeaderColumnSimple', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/headercol.h>')

    c = module.find('wxHeaderColumn')
    isinstance(c, etgtools.ClassDef)
    #c.abstract = True
    c.addAutoProperties()

    c.instanceCode = 'sipCpp = new wxHeaderColumnSimple("");'

    # addAutoProperties doesn't recognize 'IsFoo' as a getter, but it still
    # makes sense to use these, so add them manually.
    c.addProperty('Resizeable', 'IsResizeable')
    c.addProperty('Sortable', 'IsSortable')
    c.addProperty('Reorderable', 'IsReorderable')
    c.addProperty('Hidden', 'IsHidden')
    c.addProperty('Shown', 'IsShown')
    c.addProperty('SortOrderAscending', 'IsSortOrderAscending')
    c.addProperty('SortKey', 'IsSortKey')


    c = module.find('wxSettableHeaderColumn')
    #c.abstract = True
    c.addAutoProperties()

    # This class adds some setters to go with the getters (and IsFoo) methods
    # in the base class, but we can't make properties without them being in
    # the current class, so we'll monkey-patch in the properties from Python
    # code instead.
    c.addPyProperty('Title', 'HeaderColumn.GetTitle', 'SetTitle')
    c.addPyProperty('Bitmap', 'HeaderColumn.GetBitmap', 'SetBitmap')
    c.addPyProperty('Width', 'HeaderColumn.GetWidth', 'SetWidth')
    c.addPyProperty('MinWidth', 'HeaderColumn.GetMinWidth', 'SetMinWidth')
    c.addPyProperty('Alignment', 'HeaderColumn.GetAlignment', 'SetAlignment')
    c.addPyProperty('Flags', 'HeaderColumn.GetFlags', 'SetFlags')

    c.addPyProperty('Resizeable', 'HeaderColumn.IsResizeable', 'SetResizeable')
    c.addPyProperty('Sortable', 'HeaderColumn.IsSortable', 'SetSortable')
    c.addPyProperty('Reorderable', 'HeaderColumn.IsReorderable', 'SetReorderable')
    c.addPyProperty('Hidden', 'HeaderColumn.IsHidden', 'SetHidden')


    c = module.find('wxHeaderColumnSimple')
    c.addAutoProperties()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

