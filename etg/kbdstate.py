#---------------------------------------------------------------------------
# Name:        etg/kbdstate.py
# Author:      Robin Dunn
#
# Created:     15-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "kbdstate"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxKeyboardState' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxKeyboardState')
    assert isinstance(c, etgtools.ClassDef)

    c.addProperty("controlDown ControlDown SetControlDown")
    c.addProperty("rawControlDown RawControlDown SetRawControlDown")
    c.addProperty("shiftDown   ShiftDown   SetShiftDown")
    c.addProperty("altDown     AltDown     SetAltDown")
    c.addProperty("metaDown    MetaDown    SetMetaDown")
    c.addProperty("cmdDown     CmdDown")

    c.addPyCode("""\
        # For 2.8 compatibility
        KeyboardState.m_controlDown = wx.deprecated(KeyboardState.controlDown, "Use controlDown instead.")
        KeyboardState.m_shiftDown   = wx.deprecated(KeyboardState.shiftDown, "Use shiftDown instead.")
        KeyboardState.m_altDown     = wx.deprecated(KeyboardState.altDown, "Use altDown instead.")
        KeyboardState.m_metaDown    = wx.deprecated(KeyboardState.metaDown, "Use metaDown instead.")
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

