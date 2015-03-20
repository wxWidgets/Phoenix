#---------------------------------------------------------------------------
# Name:        etg/vscrol.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2011
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import WigCode

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "vscroll"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxVarScrollHelperBase",
           "wxVarVScrollHelper",
           "wxVarHScrollHelper",
           "wxVarHVScrollHelper",
           "wxVScrolledWindow",
           "wxHScrolledWindow",
           "wxHVScrolledWindow",
           ]    

KEEP_ALL = False

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    
    if KEEP_ALL:
        # First (more like 3rd...) attempt. Try to keep all the classes and
        # virtuals available to Python, and untangle things using SIP's
        # directive's etc. as needed
    
        c = module.find('wxVarScrollHelperBase')
        assert isinstance(c, etgtools.ClassDef)
        c.find('OnGetUnitsSizeHint').ignore(False)
        c.find('EstimateTotalSize').ignore(False)
        c.find('OnGetUnitSize').ignore(False)
    
    
        # Ensure that SIP knows that there are implementations of these base
        # class virtual methods in each of the two helper classes below.
        baseVirtuals = """\
        virtual void OnGetUnitsSizeHint(size_t unitMin, size_t unitMax) const;
        virtual wxCoord EstimateTotalSize() const;
        virtual int GetNonOrientationTargetSize() const;
        virtual wxOrientation GetOrientation() const;
        virtual int GetOrientationTargetSize() const;
        virtual wxCoord OnGetUnitSize(size_t unit) const;
        """
    
        c = module.find('wxVarVScrollHelper')
        c.addItem(WigCode(baseVirtuals, protection='protected'))
        c.find('EstimateTotalHeight').ignore(False)
        c.find('OnGetRowsHeightHint').ignore(False)
        c.find('OnGetRowHeight').ignore(False)
        c.find('RefreshRows.from').name = 'from_'
        c.find('RefreshRows.to').name = 'to_'
    
        c = module.find('wxVarHScrollHelper')
        c.addItem(WigCode(baseVirtuals, protection='protected'))
        c.find('EstimateTotalWidth').ignore(False)
        c.find('OnGetColumnsWidthHint').ignore(False)
        c.find('OnGetColumnWidth').ignore(False)
        c.find('RefreshColumns.from').name = 'from_'
        c.find('RefreshColumns.to').name = 'to_'
    
    
    
        c = module.find('wxVarHVScrollHelper')
        # This class is the bottom of a diamond inheritance hierarchy, and since
        # the same virtual methods may be inherited from both sides we need to
        # help the generator know which version of the methods to call.
        def _baseVirtualHints(decl, impl):
            code = """\
            {decl}
            %MethodCode
                {impl}
            %End
            %VirtualCallCode
                {impl}
            %End
            """.format(**locals())
            return code
        
        for decl, impl in [
                    ('virtual wxCoord OnGetUnitSize(size_t unit) const;',
                     'sipRes = wxVarVScrollHelper::OnGetUnitSize(unit);'),
                           
                    ('virtual void OnGetUnitsSizeHint(size_t unitMin, size_t unitMax) const;',
                     'wxVarVScrollHelper::OnGetUnitsSizeHint(unitMin, unitMax);'),
    
                    ('virtual wxCoord EstimateTotalSize() const;',
                     'sipRes = wxVarVScrollHelper::EstimateTotalSize();'),
    
                    ('virtual wxOrientation GetOrientation() const;',
                     'sipRes = wxVarVScrollHelper::GetOrientation();'),
                       
                    ('virtual int GetOrientationTargetSize() const;',
                     'sipRes = wxVarVScrollHelper::GetOrientationTargetSize();'),
                       
                    ('virtual int GetNonOrientationTargetSize() const;',
                     'sipRes = wxVarVScrollHelper::GetNonOrientationTargetSize();'),
                    ]:    
            c.addItem(WigCode(_baseVirtualHints(decl, impl), protection='protected'))
    
        for decl, impl in [
                    ('virtual void UpdateScrollbar();',
                     'wxVarVScrollHelper::UpdateScrollbar();'),
        
                    ('virtual wxWindow* GetTargetWindow() const;',
                     'sipRes = wxVarVScrollHelper::GetTargetWindow();'),  
            
                    ('virtual void SetTargetWindow(wxWindow* target);',
                     'wxVarVScrollHelper::SetTargetWindow(target);'),
    
                    ('virtual void RefreshAll();',
                     'wxVarVScrollHelper::RefreshAll();'),
            ]:    
            c.addItem(WigCode(_baseVirtualHints(decl, impl), protection='public'))
    
    
        c = module.find('wxVScrolledWindow')
        tools.fixWindowClass(c)
       
        c = module.find('wxHScrolledWindow')
        tools.fixWindowClass(c)
       
        #c = module.find('wxHVScrolledWindow')
        #tools.fixWindowClass(c)
    
    else:
        # This version will surgically exclude or unvirtualize things that
        # may be less important to Python code, in order to untangle the
        # multiple inheritance mess.

        c = module.find('wxVarScrollHelperBase')
        assert isinstance(c, etgtools.ClassDef)
        c.abstract = True
        c.find('OnGetUnitsSizeHint').ignore()
        c.find('OnGetUnitSize').ignore()
        c.find('EstimateTotalSize').ignore()
        
        c.find('GetOrientation').ignore()
        c.find('GetOrientationTargetSize').ignore()
        c.find('GetNonOrientationTargetSize').ignore()
        
        c.find('GetTargetWindow').isVirtual = False
        c.find('SetTargetWindow').isVirtual = False
        c.find('RefreshAll').isVirtual = False
        c.find('UpdateScrollbar').isVirtual = False
    
        # Ensure that SIP knows that there are implementations of these base
        # class virtual methods in each of the two helper classes below.
        baseVirtuals = """\
        // virtual wxOrientation GetOrientation() const;
        // virtual int GetOrientationTargetSize() const;
        // virtual int GetNonOrientationTargetSize() const;
        """       
    
        c = module.find('wxVarVScrollHelper')
        c.addItem(WigCode(baseVirtuals, protection='protected'))
        c.find('EstimateTotalHeight').ignore(False)
        c.find('OnGetRowsHeightHint').ignore(False)
        c.find('OnGetRowHeight').ignore(False)
        c.find('RefreshRows.from').name = 'from_'
        c.find('RefreshRows.to').name = 'to_'
    
        c = module.find('wxVarHScrollHelper')
        c.addItem(WigCode(baseVirtuals, protection='protected'))
        c.find('EstimateTotalWidth').ignore(False)
        c.find('OnGetColumnsWidthHint').ignore(False)
        c.find('OnGetColumnWidth').ignore(False)
        c.find('RefreshColumns.from').name = 'from_'
        c.find('RefreshColumns.to').name = 'to_'



        c = module.find('wxVarHVScrollHelper')


        c = module.find('wxVScrolledWindow')
        tools.fixWindowClass(c)
       
        c = module.find('wxHScrolledWindow')
        tools.fixWindowClass(c)
       
        c = module.find('wxHVScrolledWindow')
        tools.fixWindowClass(c)
        
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

