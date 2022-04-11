#---------------------------------------------------------------------------
# Name:        etg/timer.py
# Author:      Robin Dunn
#
# Created:     21-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "timer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxTimer',
           'wxTimerRunner',
           'wxTimerEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTimer')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    c = module.find('wxTimerRunner')
    c.mustHaveApp()
    c.addPrivateCopyCtor()

    module.addPyCode('EVT_TIMER = wx.PyEventBinder( wxEVT_TIMER )')

    module.addPyCode("""\
    class PyTimer(Timer):
        '''This timer class is passed the callable object to be called when the timer expires.'''
        def __init__(self, notify):
            Timer.__init__(self)
            self.notify = notify

        def Notify(self):
            if self.notify:
                self.notify()
    """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

