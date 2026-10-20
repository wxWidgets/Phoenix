#---------------------------------------------------------------------------
# Name:        etg/tipwin.py
# Author:      Robin Dunn
#
# Created:     15-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "tipwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTipWindow",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTipWindow')
    assert isinstance(c, etgtools.ClassDef)

    # The C++ ctor is deprecated because of a race with its windowPtr
    # parameter. We never expose windowPtr, so provide an equivalent ctor
    # that uses two-step creation instead of calling the deprecated one.
    c.find('wxTipWindow').findOverload('windowPtr').ignore()
    c.addCppCtor_sip(
        argsString="""(
            wxWindow* parent /TransferThis/,
            const wxString& text,
            wxCoord maxLength = 100,
            wxRect* rectBounds = NULL)
            """,
        pyArgsString="(parent, text, maxLength=100, rectBounds=None)",
        doc="""\
            Create the tip window and show it immediately.

            The tip window closes and destroys itself when the user clicks the
            mouse or presses a key, when it loses focus, or when the mouse
            leaves rectBounds (in screen coordinates) if one is given.
            """,
        body="""\
            sipCpp = new sipwxTipWindow();
            sipCpp->Create(parent, *text, maxLength, NULL, rectBounds);
            """)

    c.find('Create.windowPtr').ignore()
    c.find('Create').setCppCode_sip(
        "sipRes = sipCpp->Create(parent, *text, maxLength, NULL, rectBounds);")

    tools.fixWindowClass(c)

    # ignore this method too
    c.find('SetTipWindowPtr').ignore()

    # wxTipWindow::Close() isn't in the interface docs, so without this
    # Python would get wxWindow::Close, which doesn't close the tip.
    c.addCppMethod('bool', 'Close', '(bool force=false)',
        doc="""\
            Hide and destroy the tip window. The force parameter is ignored,
            closing a tip window can't be vetoed. Does nothing if the tip
            window has already been closed.""",
        body="""\
            if ( !wxPendingDelete.Member(self) )
                self->Close();
            return true;
            """)

    # The tip may close itself at any moment, but it isn't destroyed until
    # the next idle time, so also check that it is still shown.
    c.addPyMethod('__bool__', '(self)',
        doc="Returns True if the tip window still exists and hasn't been closed.",
        body="""\
            import wx.siplib
            return not wx.siplib.isdeleted(self) and self.IsShown()
            """)

    # Ignore the wxTipWindow::Ref class for now
    c.find('Ref').ignore()
    c.find('New').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

