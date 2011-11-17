#---------------------------------------------------------------------------
# Name:        etg/_core.py
# Author:      Robin Dunn
#
# Created:     8-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx" 
MODULE    = "_core"
NAME      = "_core"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ ]    
    

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These items are in their own etg scripts
# for easier maintainability, but their class and function definitions are
# intended to be part of this module, not their own module. This also makes it
# easier to promote one of these to module status later if desired, simply
# remove it from this list of Includes, and change the MODULE value in the
# promoted script to be the same as its NAME.

INCLUDES = [  'defs',
              'wxpy_utils',
              'string',
              'arrays',
              'clntdata',
              'userdata',
              'stockgdi',
              
              'windowid',
              'platinfo',
              'display',
              'vidmode',
              'intl',
              
              'cmndata',
              'object',
              'gdicmn',
              'geometry',

              'image',
              'gdiobj',
              'bitmap',
              'icon', 'iconloc', 'iconbndl',
              'font',
              'fontutil',
              'pen',
              'brush',
              'cursor',
              'region',
              'dc',
              'dcclient',
              'dcmemory',
              'dcbuffer',
              'dcscreen',
              'dcgraph',
              'dcmirror',
              'dcprint',
              'dcps',
              'dcsvg',
              'graphics',
              
              'accel',
              'log',
              'dataobj',
              'config',
              'variant',
              'colour',
              'tracker',
              'kbdstate',
              'mousestate',
              'tooltip',
              'layout',
              'event',
              'pyevent',
              'process',
              'utils',
              'sizer',
              'wrapsizer',
              
              'evtloop',
              'apptrait',
              'app',
              
              'timer',
              'window',
              'validate',
              'panel',
              'menu',
              'menuitem',
              
              # toplevel and dialogs
              'nonownedwnd',
              'toplevel',
              'dialog',
              'dirdlg',
              'filedlg',
              'frame',
              'msgdlg',
              'progdlg',
              
              # controls
              'statbmp',
              'stattext',
              'statbox',
              'control',
              'ctrlsub',
              'choice',
              'anybutton',
              'button',
              'bmpbuttn',
              'withimage',
              'bookctrl',
              'notebook',
              'imaglist',
              'splitter',
              'collpane',
              'statline',
              'stdpaths',
              'snglinst',
              'textcompleter',
              'textentry',
              'textctrl',
              'combobox',
              'checkbox',
              'checklst',
              'listbox',
              'gauge',
              'headercol',
              'srchctrl',
              'radiobox', 
              'radiobut',
              'scrolwin',
              'slider',
              'spinbutt',
              'spinctrl',
              'tglbtn',
              'statusbar',
              ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from setup.py for a list of sources and a list
# of additional dependencies when building this extension module
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [ 'src/core_ex.py',
              'src/core_ex.cpp' ]


#---------------------------------------------------------------------------
 
def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode("""\
    #if defined(__APPLE__)
        // When it's possible that we're building universal binaries with both
        // 32-bit and 64-bit architectures then these need to be undefed because
        // otherwise the values set by configure could conflict with those set
        // based on runtime flags in Python's headers.  We also do something
        // similar in wx/platform.h so it's okay to undef them now because they
        // will be defined again soon.
        #undef SIZEOF_VOID_P
        #undef SIZEOF_LONG
        #undef SIZEOF_SIZE_T

        // Turn off the warning about converting string literals to char*
        // TODO: fix these the right way...
        #pragma GCC diagnostic ignored "-Wwrite-strings"
    #endif
    #ifdef _MSC_VER
        #pragma warning(disable:4800)
        #pragma warning(disable:4190)
    #endif
    
    #include <wx/wx.h>
    """)
    
    module.includePyCode('src/core_ex.py', order=10)
    
    module.addInclude(INCLUDES)
    
    # This code is inserted into the module initialization function
    module.addPostInitializerCode("""\
        wxPyCoreModuleInject(sipModuleDict);
        """)
    # Here is the function it calls
    module.includeCppCode('src/core_ex.cpp')
                      
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
