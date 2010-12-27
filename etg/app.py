#---------------------------------------------------------------------------
# Name:        etg/app.py
# Author:      Robin Dunn
#
# Created:     22-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "app"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxAppConsole',
           'wxApp',           
           ]    

OTHERDEPS = [ 'src/app_ex.py',    # Some extra app-related Python code
              'src/app_ex.cpp',   # and some C++ code too
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
        
    c = module.find('wxAppConsole')
    assert isinstance(c, etgtools.ClassDef)
    
    # There's no need for the command line stuff as Python has its own ways to
    # deal with that
    c.find('argc').ignore()
    c.find('argv').ignore()    
    c.find('OnCmdLineError').ignore()
    c.find('OnCmdLineHelp').ignore()
    c.find('OnCmdLineParsed').ignore()
    c.find('OnInitCmdLine').ignore()
    
    c.find('HandleEvent').ignore()
    c.find('UsesEventLoop').ignore()
    

    # We will use OnAssertFailure, but I don't think we should let it be
    # overridden in Python. 
    c.find('OnAssertFailure').ignore()
    
    # TODO: Decide if these should be visible from Python. They are for
    # dealing with C/C++ exceptions, but perhaps we could also add the ability
    # to deal with unhandled Python exceptions using these (overridable)
    # methods too.
    c.find('OnExceptionInMainLoop').ignore()
    c.find('OnFatalException').ignore()
    c.find('OnUnhandledException').ignore()
    
    c.find('ExitMainLoop').isVirtual = False
    
    
    c.addProperty('AppDisplayName GetAppDisplayName SetAppDisplayName')
    c.addProperty('AppName GetAppName SetAppName')
    c.addProperty('ClassName GetClassName SetClassName')
    c.addProperty('VendorDisplayName GetVendorDisplayName SetVendorDisplayName')
    c.addProperty('VendorName GetVendorName SetVendorName')
    
    
    #-------------------------------------------------------
    c = module.find('wxApp')
    
    # Add a new C++ wxPyApp class that adds empty Mac* methods for other
    # platforms, and other goodies, then change the c.name so SIP will
    # generate code wrapping this class as if it was the wxApp class seen in
    # the DoxyXML. 
    c.includeCppCode('src/app_ex.cpp')
    
    # Now change the class name, ctors and dtor names from wxApp to wxPyApp
    for item in c.allItems():  
        if item.name == 'wxApp':
            item.name = 'wxPyApp' 
        if item.name == '~wxApp':
            item.name = '~wxPyApp'
    
    c.find('ProcessMessage').ignore()
    
     
    c.addCppMethod('void', 'MacHideApp', '()',
        doc="Hide all application windows just as the user can do with the\nsystem Hide command.  Mac only.",
        body="""\
        #ifdef __WXMAC__
            self->MacHideApp();
        #endif
        """)

    # Remove the virtualness from these methods
    for m in [ 'GetDisplayMode', 'GetLayoutDirection', 'GetTopWindow', 'IsActive', 
               'SafeYield', 'SafeYieldFor', 'SendIdleEvents', 'SetDisplayMode', 
               'SetNativeTheme', ]:
        c.find(m).isVirtual = False
    
    # Methods we implement in wxPyApp beyond what are in wxApp, plus some
    # overridden virtuals (or at least some that we want the wrapper generator
    # to treat as if they are overridden.)
    c.addItem(etgtools.WigCode("""\
        wxAppAssertMode GetAssertMode();
        void            SetAssertMode(wxAppAssertMode mode);
        void            _BootstrapApp();
        static bool     IsDisplayAvailable();
        
        virtual int  MainLoop();
        virtual void OnPreInit();
        virtual bool OnInit();
        virtual bool OnInitGui();
        virtual int  OnRun();
        virtual int  OnExit();
        """))
        

    c.addProperty('DisplayMode GetDisplayMode SetDisplayMode')
    c.addProperty('ExitOnFrameDelete GetExitOnFrameDelete SetExitOnFrameDelete')
    c.addProperty('LayoutDirection GetLayoutDirection')
    c.addProperty('UseBestVisual GetUseBestVisual SetUseBestVisual')
    c.addProperty('TopWindow GetTopWindow SetTopWindow')
    
    
    
    appHeaderCode = """\
        enum wxAppAssertMode {
            wxPYAPP_ASSERT_SUPPRESS  = 1,
            wxPYAPP_ASSERT_EXCEPTION = 2,
            wxPYAPP_ASSERT_DIALOG    = 4,
            wxPYAPP_ASSERT_LOG       = 8
        };
        """
    # Add it to both the header and the generator files
    module.insertItemBefore(c, etgtools.WigCode(appHeaderCode))
    module.addHeaderCode(appHeaderCode)
    module.addHeaderCode("""\
        class wxPyApp;
        wxPyApp* wxGetApp();
        """)
    module.insertItemAfter(c, etgtools.WigCode("""\
        wxPyApp* wxGetApp();
        """))
    
    
    # This includes Python code for the on-demand output window, the Python
    # derived wx.App class, etc.
    module.includePyCode('src/app_ex.py')
    

    module.find('wxTheApp').ignore()
    module.find('wxGetApp').ignore()
    module.find('wxInitialize').ignore()
    module.find('wxUninitialize').ignore()

    for item in module.allItems():
        if item.name == 'wxEntry':
            item.ignore()
                

    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------


if __name__ == '__main__':
    run()

