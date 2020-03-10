#---------------------------------------------------------------------------
# Name:        etg/evtloop.py
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
NAME      = "evtloop"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxEventLoopBase',
           'wxEventLoopActivator',
           'wxGUIEventLoop',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False  # wxEventLoop is well tested in
                                                      # myYield used by other tests...
                                )
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxEventLoopBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    c.find('Yield').releaseGIL()
    c.find('YieldFor').releaseGIL()
    c.find('OnExit').ignore(False)


    c = module.find('wxEventLoopActivator')
    c.addPrivateAssignOp()
    c.addPrivateCopyCtor()

    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')



    c = module.find('wxGUIEventLoop')
    c.addPrivateCopyCtor()

    # Add declaration of the base class pure virtuals so sip knows they have
    # implementations here
    c.addItem(etgtools.WigCode("""\
        public:
        virtual int Run();
        virtual void Exit(int rc = 0);
        virtual void ScheduleExit(int rc = 0);
        virtual bool Pending() const;
        virtual bool Dispatch();
        virtual int DispatchTimeout(unsigned long timeout);
        virtual void WakeUp();
        virtual bool YieldFor(long eventsToProcess);
        """))

    module.addPyCode("""\
        @wx.deprecatedMsg('Use GUIEventLoop instead.')
        class EventLoop(GUIEventLoop):
            '''A class using the old name for compatibility.'''
            def __init__(self):
                GUIEventLoop.__init__(self)
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

