#---------------------------------------------------------------------------
# Name:        _core.py
# Author:      Robin Dunn
#
# Created:     8-Nove-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "_core"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
    'defs_8h.xml'
]    
    
#---------------------------------------------------------------------------
# Parse the XML file(s) building a collection of Extractor objects

import etgtools
import etgtools.tweaker_tools as tools

module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
etgtools.parseDoxyXML(module, ITEMS)

#---------------------------------------------------------------------------
# Tweak the parsed meta objects in the module object as needed for customizing
# the generated code and docstrings.


module.addHeaderCode('#include <wx/wx.h>')


# These items are in their own etg scripts for easier maintainability,
# but their class and function definitions are intended to be part of
# this module, not their own module.  This also makes it easier to
# promote one of these to module status later if desired, simply
# remove it fron this list of Includes, and change the MODULE value in
# the promoted script to be the same as its NAME.

module.addInclude(['string',
                   'clntdata',
                   'windowid',
                   'object',
                   
                   'tracker',
                   'kbdstate',
                   'mousestate',
                   'event',
                   
                   'gdicmn',
                   'geometry',

                   ])


# tweaks for defs.h
module.find('wxInt16').type = 'short'
module.find('wxInt64').type = 'long long'
module.find('wxUint64').type = 'unsigned long long'
module.find('wxIntPtr').type =  'long'           #'ssize_t'
module.find('wxUIntPtr').type = 'unsigned long'  #'size_t'

module.find('wxDELETE').ignore()
module.find('wxDELETEA').ignore()
module.find('wxSwap').ignore()
module.find('wxVaCopy').ignore()

# add some typedefs for wxChar, wxUChar
td = module.find('wxUIntPtr')
module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxUChar'))
module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxChar'))



#---------------------------------------------------------------------------
tools.ignoreAssignmentOperators(module)
tools.removeWxPrefixes(module)
#---------------------------------------------------------------------------
# Run the generators

# Create the code generator and make the wrapper code
wg = etgtools.getWrapperGenerator()
wg.generate(module)

# Create a documentation generator and let it do its thing
dg = etgtools.getDocsGenerator()
dg.generate(module)

#---------------------------------------------------------------------------
