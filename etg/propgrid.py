#---------------------------------------------------------------------------
# Name:        etg/propgrid.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgrid"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'interface_2wx_2propgrid_2propgrid_8h.xml',
           'wxPGValidationInfo',
           'wxPropertyGrid',
           'wxPropertyGridEvent',
           'wxPropertyGridPopulator',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPGValidationInfo')
    assert isinstance(c, etgtools.ClassDef)


    c = module.find('wxPropertyGrid')
    assert isinstance(c, etgtools.ClassDef)
    c.bases[0] = 'wxControl'  # sip can't handle wxScrolled<wxControl>. See also below.
    tools.fixWindowClass(c, False)
    module.addGlobalStr('wxPropertyGridNameStr', c)

    for name in ['RegisterEditorClass', 'DoRegisterEditorClass']:
        for m in c.find(name).all():
            m.find('editor').transfer = True


    # TODO: provide a way to use a Python callable as a sort function
    c.find('GetSortFunction').ignore()
    c.find('SetSortFunction').ignore()
    module.find('wxPGSortCallback').ignore()

    # Add some extra Python code to be executed when a wxPropertyGrid is
    # constructed. In Classic with SWIG we did this with %pythonAppend, is
    # there any better way to do it with sip than monkey-patching?
    c.addPyCode("""\
        _PropertyGrid__init__orig = PropertyGrid.__init__
        def _PropertyGrid__init__(self, *args, **kw):
            _PropertyGrid__init__orig(self, *args, **kw)
            self.DoDefaultTypeMappings()
            self.edited_objects = {}
            self.DoDefaultValueTypeMappings()
            if not hasattr(self.__class__, '_vt2setter'):
                self.__class__._vt2setter = {}
        PropertyGrid.__init__ = _PropertyGrid__init__
        """)

    # See note in propgridiface.py
    for item in module.allItems():
        if hasattr(item, 'type') and item.type == 'wxPGPropArg':
            item.type = 'const wxPGPropArgCls &'

    # We can't let sip create a wxScrolledControl via a typedef because of the
    # differences in the parameters of the Create methods, so instead let's just
    # copy the method definitions from wxScrolled<> here and let the compiler
    # sort it out.
    import scrolwin
    mod = scrolwin.parseAndTweakModule()
    klass = mod.find('wxScrolled')
    newItems = [item for item in klass.items
        if not c.findItem(item.name) and not item.isCtor]
    c.items.extend(newItems)



    c = module.find('wxPropertyGridEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_PG_CHANGED = wx.PyEventBinder( wxEVT_PG_CHANGED, 1 )
        EVT_PG_CHANGING = wx.PyEventBinder( wxEVT_PG_CHANGING, 1 )
        EVT_PG_SELECTED = wx.PyEventBinder( wxEVT_PG_SELECTED, 1 )
        EVT_PG_HIGHLIGHTED = wx.PyEventBinder( wxEVT_PG_HIGHLIGHTED, 1 )
        EVT_PG_RIGHT_CLICK = wx.PyEventBinder( wxEVT_PG_RIGHT_CLICK, 1 )
        EVT_PG_PAGE_CHANGED = wx.PyEventBinder( wxEVT_PG_PAGE_CHANGED, 1 )
        EVT_PG_ITEM_COLLAPSED = wx.PyEventBinder( wxEVT_PG_ITEM_COLLAPSED, 1 )
        EVT_PG_ITEM_EXPANDED = wx.PyEventBinder( wxEVT_PG_ITEM_EXPANDED, 1 )
        EVT_PG_DOUBLE_CLICK = wx.PyEventBinder( wxEVT_PG_DOUBLE_CLICK, 1 )
        EVT_PG_LABEL_EDIT_BEGIN = wx.PyEventBinder( wxEVT_PG_LABEL_EDIT_BEGIN, 1 )
        EVT_PG_LABEL_EDIT_ENDING = wx.PyEventBinder( wxEVT_PG_LABEL_EDIT_ENDING, 1 )
        EVT_PG_COL_BEGIN_DRAG = wx.PyEventBinder( wxEVT_PG_COL_BEGIN_DRAG, 1 )
        EVT_PG_COL_DRAGGING = wx.PyEventBinder( wxEVT_PG_COL_DRAGGING, 1 )
        EVT_PG_COL_END_DRAG = wx.PyEventBinder( wxEVT_PG_COL_END_DRAG, 1 )
        """)


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')


    # Switch wxPGVFBFlags to unsigned char
    td = module.find('wxPGVFBFlags')
    td.ignore()

    for name in ['wxPGValidationInfo.GetFailureBehavior',
                 'wxPGValidationInfo.SetFailureBehavior.failureBehavior',
                 'wxPropertyGridEvent.GetValidationFailureBehavior',
                 'wxPropertyGridEvent.SetValidationFailureBehavior.flags',
                ]:
        item = module.find(name)
        assert item.type == 'wxPGVFBFlags'
        item.type = 'byte'



    c = module.find('wxPropertyGridPopulator')
    tools.ignoreConstOverloads(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

