#---------------------------------------------------------------------------
# Name:        etg/srchctrl.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "srchctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxSearchCtrl' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/srchctrl.h>')

    c = module.find('wxSearchCtrl')
    assert isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxSearchCtrlNameStr', c)

    c.find('SetMenu.menu').transfer = True

    c.addCppMethod('void', 'SetSearchBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchBitmap(*bmp);
            #endif
            """)
    c.addCppMethod('void', 'SetSearchMenuBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchMenuBitmap(*bmp);
            #endif
            """)
    c.addCppMethod('void', 'SetCancelBitmap', '(const wxBitmap* bmp)',
            """\
            #ifdef __WXMAC__
            #else
                self->SetSearchMenuBitmap(*bmp);
            #endif
            """)

    searchCtrl = c


    # The safest way to reconcile the differences in the class hierachy
    # between the native wxSearchCtrl on Mac and the generic one on the other
    # platforms is to just say that this class derives directly from
    # wxControl (the first common ancestor) instead of wxTextCtrl, and then
    # redeclare all the wxTextEntry and/or wxTextCtrlIface methods that we
    # are interested in having here. That way the C++ compiler can sort out
    # the proper way to call those methods and avoid calling the wrong
    # implementations like would happen if try to force it another way...
    searchCtrl.bases = ['wxControl']

    # Instead of duplicating those declarations here, let's use the parser
    # and tweakers we already have and then just transplant those MethodDefs
    # into this ClassDef. That will then preserve things like the
    # documentation and custom tweaks that would be real tedious to duplicate
    # and maintain.
    import textentry
    mod = textentry.parseAndTweakModule()
    klass = mod.find('wxTextEntry')
    searchCtrl.items.extend(klass.items)

    # Do the same with wxTextCtrl, but also remove things like the
    # Constructors and Create methods first.
    import textctrl
    mod = textctrl.parseAndTweakModule()
    klass = mod.find('wxTextCtrl')
    # get just the methods that are not ctors, dtor or Create
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             item.name != 'Create']
    searchCtrl.items.extend(items)


    searchCtrl.find('LoadFile').ignore()
    searchCtrl.find('SaveFile').ignore()
    searchCtrl.find('MacCheckSpelling').ignore()
    searchCtrl.find('ShowNativeCaret').ignore()
    searchCtrl.find('HideNativeCaret').ignore()


    # Add some properties that autoProperties would not see because they are
    # not using 'Get' and 'Set'
    searchCtrl.addProperty('SearchButtonVisible IsSearchButtonVisible ShowSearchButton')
    searchCtrl.addProperty('CancelButtonVisible IsCancelButtonVisible ShowCancelButton')
    searchCtrl.addAutoProperties()
    tools.fixWindowClass(searchCtrl)

    module.addPyCode("""\
        EVT_SEARCHCTRL_CANCEL_BTN = wx.PyEventBinder( wxEVT_SEARCHCTRL_CANCEL_BTN, 1)
        EVT_SEARCHCTRL_SEARCH_BTN = wx.PyEventBinder( wxEVT_SEARCHCTRL_SEARCH_BTN, 1)

        # deprecated wxEVT aliases
        wxEVT_COMMAND_SEARCHCTRL_CANCEL_BTN  = wxEVT_SEARCHCTRL_CANCEL_BTN
        wxEVT_COMMAND_SEARCHCTRL_SEARCH_BTN  = wxEVT_SEARCHCTRL_SEARCH_BTN
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

