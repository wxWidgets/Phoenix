#---------------------------------------------------------------------------
# Name:        etg/progdlg
# Author:      Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
import copy

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "progdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxGenericProgressDialog',
           'wxProgressDialog'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/progdlg.h>")

    c = gpd = module.find('wxGenericProgressDialog')
    assert isinstance(c, etgtools.ClassDef)

    tools.fixWindowClass(c)#, False)
    #tools.removeVirtuals(c)

    c.find('Pulse.skip').out = True
    c.find('Update.skip').out = True

    # The C++ docs describe the bool return value, but skip is an output too
    m = c.find('Update')
    m.detailedDoc[0:2] = [
        'Returns a tuple ``(continue, skip)``. ``continue`` is ``True`` unless '
        'the "Cancel" button has been pressed, and ``skip`` is ``True`` if the '
        '"Skip" button has been pressed since the last call.',
        'If ``continue`` is ``False``, the application can either immediately '
        'destroy the dialog or ask the user for the confirmation and if the '
        'abort is not confirmed the dialog may be resumed with :meth:`Resume`.']
    c.find('Pulse').detailedDoc.insert(
        1, 'Returns a tuple ``(continue, skip)``, like :meth:`Update`.')


    c = module.find('wxProgressDialog')

    # Copy methods from the generic to the native class. This is needed
    # because none of the methods are declared in the interface files, and
    # since on MSW some non-virtual methods are reimplemented in
    # wxProgressDialogs they will not be called if SIP doesn't know about
    # them. We'll copy all of them and let the C++ compiler sort things out.
    for item in gpd:
        if (isinstance(item, etgtools.MethodDef) and
                not item.isCtor and
                not item.isDtor):
            c.addItem(copy.deepcopy(item))

    # On MSW, ~wxProgressDialog waits for the native task dialog's thread to
    # end and then enables the windows the dialog disabled. Destroy() would
    # only delete it later, inside the next modal dialog's event loop, and
    # that dialog would then not be modal any more. This must be the virtual
    # that fixWindowClass() declares, as SIP would call that one instead.
    m = etgtools.MethodDef(
        protection='public', type='bool', name='Destroy', argsString='()',
        briefDoc="""\
            Destroys the dialog. On Windows the dialog is deleted right away,
            so that the windows it disabled are enabled again before the next
            dialog is shown, rather than later like with other top-level
            windows.""",
        className=c.name)
    m.setCppCode_sip("""\
        Py_BEGIN_ALLOW_THREADS
        #ifdef __WXMSW__
            delete sipCpp;
            sipRes = true;
        #else
            sipRes = sipSelfWasArg ? sipCpp->::wxProgressDialog::Destroy()
                                   : sipCpp->Destroy();
        #endif
        Py_END_ALLOW_THREADS
        """)
    c.addItem(m)

    tools.fixWindowClass(c)

    # wx only sets skip when it is false on input, so it must start out false
    for klass in (gpd, c):
        name = klass.name
        klass.find('Update').setCppCode_sip(f"""\
            skip = false;
            sipRes = sipSelfWasArg ? sipCpp->::{name}::Update(value, *newmsg, &skip)
                                   : sipCpp->Update(value, *newmsg, &skip);
            """)
        klass.find('Pulse').setCppCode_sip(f"""\
            skip = false;
            sipRes = sipSelfWasArg ? sipCpp->::{name}::Pulse(*newmsg, &skip)
                                   : sipCpp->Pulse(*newmsg, &skip);
            """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

