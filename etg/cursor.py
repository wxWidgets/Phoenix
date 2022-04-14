#---------------------------------------------------------------------------
# Name:        etg/cursor.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     06-Sept-2011
# Copyright:   (c) 2013 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "cursor"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxCursor', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxCursor')
    assert isinstance(c, etgtools.ClassDef)

    # Set mustHaveApp on all ctors except the default ctor
    for ctor in c.find('wxCursor').all():
        if ctor.isCtor and ctor.argsString != '()':
            ctor.mustHaveApp()


    c.find('wxCursor').findOverload('bits').ignore()
    c.find('wxCursor').findOverload('cursorName').find('type').default='wxBITMAP_TYPE_ANY'
    # TODO: This ctor ^^ in Classic has a custom implementation for wxGTK that
    # sets the hotspot. Is that still needed?
    c.find('wxCursor').findOverload('(const char *const *xpmData)').ignore()

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('long', 'GetHandle', '()', """\
    #ifdef __WXMSW__
        return HandleToLong(self->GetHandle());
    #else
        return 0;
    #endif""",
    briefDoc="Get the handle for the Cursor.  Windows only.")

    c.addCppMethod('void', 'SetHandle', '(long handle)', """\
    #ifdef __WXMSW__
        self->SetHandle((WXHANDLE)LongToHandle(handle));
    #endif""",
    briefDoc="Set the handle to use for this Cursor.  Windows only.")

    # TODO:  Classic has MSW-only getters and setters for width, height, depth, and size.

    # The stock Cursor items are documented as simple pointers, but in reality
    # they are macros that evaluate to a function call that returns a cursor
    # pointer, and that is only valid *after* the wx.App object has been
    # created. That messes up the code that SIP generates for them, so we need
    # to come up with another solution. So instead we will just create
    # uninitialized cursor in a block of Python code, that will then be
    # initialized later when the wx.App is created.
    c.addCppMethod('void', '_copyFrom', '(const wxCursor* other)',
                   "*self = *other;",
                   briefDoc="For internal use only.")  # ??
    pycode = '# These stock cursors will be initialized when the wx.App object is created.\n'
    for item in module:
        if '_CURSOR' in item.name:
            item.ignore()
            pycode += '%s = Cursor()\n' % tools.removeWxPrefix(item.name)
    module.addPyCode(pycode)

    # former renamed constructors
    module.addPyCode('StockCursor = wx.deprecated(Cursor, "Use Cursor instead.")')
    module.addPyCode('CursorFromImage = wx.deprecated(Cursor, "Use Cursor instead.")')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

