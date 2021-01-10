#---------------------------------------------------------------------------
# Name:        etg/wizard.py
# Author:      Robin Dunn
#
# Created:     06-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools.extractors import MethodDef, ParamDef

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "wizard"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxWizardPage",
           "wxWizardPageSimple",
           "wxWizard",
           "wxWizardEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxWizardPage')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c, False)
    module.addPyCode("PyWizardPage = wx.deprecated(WizardPage, 'Use WizardPage instead.')")


    c = module.find('wxWizardPageSimple')
    tools.fixWindowClass(c, False)
    c.addItem(etgtools.WigCode("""\
        virtual wxWizardPage* GetNext() const;
        virtual wxWizardPage* GetPrev() const;
        """))


    c = module.find('wxWizard')
    tools.fixWindowClass(c, False)

    # ShowPage is undocumented and labeled "implementation only" but it seems
    # too useful to ignore, so add a MethodDef for it here.
    m = MethodDef(name='ShowPage', type='bool', isVirtual=True,
            briefDoc="Show the given wizard page.",
            detailedDoc=["""\
                Calls TransferDataFromWindow on the current page first, and
                returns false without changing the page if it returned false.
                Returns True/False to indicate if the page was actually
                changed."""],
            items=[ParamDef(name='page', type='wxWizardPage*'),
                   ParamDef(name='goingForward', type='bool', default='true')])
    c.addItem(m)

    # Same for IsRunning
    m = MethodDef(name='IsRunning', type='bool', isConst=True)
    c.addItem(m)


    c = module.find('wxWizardEvent')
    tools.fixEventClass(c)
    module.addPyCode("""\
        EVT_WIZARD_BEFORE_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_WIZARD_BEFORE_PAGE_CHANGED, 1)
        EVT_WIZARD_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_WIZARD_PAGE_CHANGED, 1)
        EVT_WIZARD_PAGE_CHANGING = wx.PyEventBinder( wxEVT_WIZARD_PAGE_CHANGING, 1)
        EVT_WIZARD_CANCEL        = wx.PyEventBinder( wxEVT_WIZARD_CANCEL, 1)
        EVT_WIZARD_HELP          = wx.PyEventBinder( wxEVT_WIZARD_HELP, 1)
        EVT_WIZARD_FINISHED      = wx.PyEventBinder( wxEVT_WIZARD_FINISHED, 1)
        EVT_WIZARD_PAGE_SHOWN    = wx.PyEventBinder( wxEVT_WIZARD_PAGE_SHOWN, 1)
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

