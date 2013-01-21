#---------------------------------------------------------------------------
# Name:        etg/clipbrd.py
# Author:      Robin Dunn
#
# Created:     09-May-2012
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "clipbrd"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxClipboard",
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxClipboard')
    assert isinstance(c, etgtools.ClassDef)
    
    c.find('AddData.data').transfer = True
    c.find('SetData.data').transfer = True

    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'self.Close()')
    
    # TODO: This init wrapper class may be useful elsewhere...
    module.addPyCode("""\
        # Since wxTheClipoard is not really a global varaiable (it is a macro 
        # that calls the Get static method) we can't declare it as a global 
        # variable for the wrapper generator, otherwise it will try to run the 
        # function at module import and the wxApp object won't exist yet.  So
        # we'll use a class that will allow us to delay calling the Get until 
        # wx.TheClipboard is actually being used for the first time.
        class _wxPyDelayedInitWrapper(object):
            def __init__(self, initfunc, *args, **kwargs):
                self._initfunc = initfunc
                self._args = args
                self._kwargs = kwargs
                self._instance = None
            def _checkInstance(self):
                if self._instance is None:
                    if wx.GetApp():
                        self._instance = self._initfunc(*self._args, **self._kwargs)        
            def __getattr__(self, name):
                self._checkInstance()
                return getattr(self._instance, name)
            def __repr__(self):
                self._checkInstance()
                return repr(self._instance)

        TheClipboard = _wxPyDelayedInitWrapper(Clipboard.Get)
        """)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

