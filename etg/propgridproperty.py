#---------------------------------------------------------------------------
# Name:        etg/property.py
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
NAME      = "propgridproperty"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPGPaintData',
           'wxPGCellRenderer',
           'wxPGDefaultRenderer',
           'wxPGCellData',
           'wxPGCell',
           'wxPGAttributeStorage',

           'wxPGProperty',
           'wxPropertyCategory',
           'wxPGChoiceEntry',
           'wxPGChoicesData',
           'wxPGChoices',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPGCellData')
    assert isinstance(c, etgtools.ClassDef)
    c.find('~wxPGCellData').ignore(False)
    c.bases = ['wxRefCounter']


    #---------------------------------------------------------
    c = module.find('wxPGCell')
    tools.ignoreConstOverloads(c)


    #---------------------------------------------------------
    c = module.find('wxPGCellRenderer')
    c.bases = ['wxRefCounter']


    #---------------------------------------------------------
    c = module.find('wxPGAttributeStorage')
    c.find('const_iterator').ignore()
    c.find('StartIteration').ignore()
    c.find('GetNext').ignore()


    #---------------------------------------------------------
    c = module.find('wxPGProperty')
    tools.ignoreConstOverloads(c)

    # The ctors are protected, so unignore them
    for ctor in c.find('wxPGProperty').all():
        ctor.ignore(False)

    c.find('StringToValue.variant').out = True
    c.find('IntToValue.variant').out = True

    c.find('HasFlag').findOverload('FlagType').ignore()

    c.addProperty('m_value GetValue SetValue')


    # SIP needs to be able to make a copy of the wxPGAttributeStorage value
    # but the C++ class doesn't have a copy ctor and the default will cause it
    # to lose references to the variants it contains, so let's just override
    # the use of the MappedType and convert it to a Python dictionary here
    # instead.
    m = c.find('GetAttributes')
    m.type = 'PyObject*'
    m.setCppCode("""\
        const wxPGAttributeStorage& attrs = self->GetAttributes();
        wxPGAttributeStorage::const_iterator it = attrs.StartIteration();
        wxVariant v;
        wxPyThreadBlocker blocker;

        PyObject* dict = PyDict_New();
        if ( !dict ) return NULL;

        while ( attrs.GetNext( it, v ) ) {
            const wxString& name = v.GetName();
            PyObject* pyStr = wx2PyString(name);
            PyObject* pyVal = wxPGVariant_out_helper(v);
            int res = PyDict_SetItem( dict, pyStr, pyVal );
        }
        return dict;
        """)

    # SetAttributes uses wxPGAttributeStorage too, but we'll just replace it
    # with a simple Python method.
    c.find('SetAttributes').ignore()
    c.addPyMethod('SetAttributes', '(self, attributes)',
        doc="Set the property's attributes from a Python dictionary.",
        body="""\
            for name,value in attributes.items():
                self.SetAttribute(name, value)
            """)

    c.find('AddPrivateChild.prop').transfer = True
    c.find('AddChild.prop').transfer = True

    # The [G|S]etClientData methods deal with untyped void* values, which we
    # don't support. The [G|S]etClientObject methods use wxClientData instances
    # which we have a MappedType for, so make the ClientData methods just be
    # aliases for ClientObjects. From the Python programmer's perspective they
    # would be virtually the same anyway.
    c.find('SetClientObject.clientObject').transfer = True
    c.find('SetClientObject.clientObject').name = 'data'
    c.find('GetClientData').ignore()
    c.find('SetClientData').ignore()
    c.find('GetClientObject').pyName = 'GetClientData'
    c.find('SetClientObject').pyName = 'SetClientData'
    c.addPyMethod('GetClientObject', '(self, n)',
        doc="Alias for :meth:`GetClientData`",
        body="return self.GetClientData(n)")
    c.addPyMethod('SetClientObject', '(self, n, data)',
        doc="Alias for :meth:`SetClientData`",
        body="self.SetClientData(n, data)")

    c.find('GetEditorDialog').factory = True

    # deprecated and removed
    c.find('AddChild').ignore()
    c.find('GetValueString').ignore()


    #---------------------------------------------------------
    c = module.find('wxPGChoicesData')
    tools.ignoreConstOverloads(c)
    c.bases = ['wxRefCounter']
    c.find('~wxPGChoicesData').ignore(False)


    #---------------------------------------------------------
    c = module.find('wxPGChoices')
    c.find('wxPGChoices').findOverload('wxChar **').ignore()
    c.find('wxPGChoices').findOverload('wxString *').ignore()
    c.find('Add').findOverload('wxChar **').ignore()
    c.find('Add').findOverload('wxString *').ignore()
    c.find('Set').findOverload('wxChar **').ignore()
    c.find('Set').findOverload('wxString *').ignore()
    tools.ignoreConstOverloads(c)
    c.find('operator[]').ignore()
    c.find('GetId').type = 'wxIntPtr'
    c.find('GetId').setCppCode_sip("""\
        sipRes = new  ::wxIntPtr((wxIntPtr)sipCpp->GetId());
        """)

    c.addPyMethod('__getitem__', '(self, index)',
        doc="Returns a reference to a :class:PGChoiceEntry using Python list syntax.",
        body="return self.Item(index)",
        )
    c.addPyMethod('__len__', '(self)',
        doc="",
        body="return self.GetCount()",
        )


    #---------------------------------------------------------
    # Ignore some string constants (#defines) coming from dox, and add them
    # back in Python code. They are wchar_t* values and this seemed the
    # simplest way to deal with them.
    for name in [ 'wxPG_ATTR_DEFAULT_VALUE',
                  'wxPG_ATTR_MIN',
                  'wxPG_ATTR_MAX',
                  'wxPG_ATTR_UNITS',
                  'wxPG_ATTR_HINT',
                  'wxPG_ATTR_AUTOCOMPLETE',
                  'wxPG_BOOL_USE_CHECKBOX',
                  'wxPG_BOOL_USE_DOUBLE_CLICK_CYCLING',
                  'wxPG_FLOAT_PRECISION',
                  'wxPG_STRING_PASSWORD',
                  'wxPG_UINT_BASE',
                  'wxPG_UINT_PREFIX',
                  'wxPG_FILE_WILDCARD',
                  'wxPG_FILE_SHOW_FULL_PATH',
                  'wxPG_FILE_SHOW_RELATIVE_PATH',
                  'wxPG_FILE_INITIAL_PATH',
                  # 'wxPG_FILE_DIALOG_TITLE',
                  'wxPG_DIALOG_TITLE',
                  'wxPG_FILE_DIALOG_STYLE',
                  # 'wxPG_DIR_DIALOG_MESSAGE',
                  'wxPG_ARRAY_DELIMITER',
                  'wxPG_DATE_FORMAT',
                  'wxPG_DATE_PICKER_STYLE',
                  'wxPG_ATTR_SPINCTRL_STEP',
                  'wxPG_ATTR_SPINCTRL_WRAP',
                  'wxPG_ATTR_SPINCTRL_MOTION',
                  'wxPG_ATTR_MULTICHOICE_USERSTRINGMODE',
                  'wxPG_COLOUR_ALLOW_CUSTOM',
                  'wxPG_COLOUR_HAS_ALPHA',

                  # and some other #defines with similar issues
                  'wxNullProperty',
                  'wxPGChoicesEmptyData',
                  ]:
        module.find(name).ignore()

        module.addPyCode("""\
            PG_ATTR_DEFAULT_VALUE             = u"DefaultValue"
            PG_ATTR_MIN                       = u"Min"
            PG_ATTR_MAX                       = u"Max"
            PG_ATTR_UNITS                     = u"Units"
            PG_ATTR_HINT                      = u"Hint"
            PG_ATTR_INLINE_HELP               = PG_ATTR_HINT
            PG_ATTR_AUTOCOMPLETE              = u"AutoComplete"
            PG_BOOL_USE_CHECKBOX              = u"UseCheckbox"
            PG_BOOL_USE_DOUBLE_CLICK_CYCLING  = u"UseDClickCycling"
            PG_FLOAT_PRECISION                = u"Precision"
            PG_STRING_PASSWORD                = u"Password"
            PG_UINT_BASE                      = u"Base"
            PG_UINT_PREFIX                    = u"Prefix"
            PG_FILE_WILDCARD                  = u"Wildcard"
            PG_FILE_SHOW_FULL_PATH            = u"ShowFullPath"
            PG_FILE_SHOW_RELATIVE_PATH        = u"ShowRelativePath"
            PG_FILE_INITIAL_PATH              = u"InitialPath"
            PG_FILE_DIALOG_TITLE              = u"DialogTitle"
            PG_DIALOG_TITLE                   = u"DialogTitle"
            PG_FILE_DIALOG_STYLE              = u"DialogStyle"
            PG_DIR_DIALOG_MESSAGE             = u"DialogMessage"
            PG_ARRAY_DELIMITER                = u"Delimiter"
            PG_DATE_FORMAT                    = u"DateFormat"
            PG_DATE_PICKER_STYLE              = u"PickerStyle"
            PG_ATTR_SPINCTRL_STEP             = u"Step"
            PG_ATTR_SPINCTRL_WRAP             = u"Wrap"
            PG_ATTR_SPINCTRL_MOTION           = u"MotionSpin"
            PG_ATTR_SPINCTRL_MOTIONSPIN       = PG_ATTR_SPINCTRL_MOTION
            PG_ATTR_MULTICHOICE_USERSTRINGMODE= u"UserStringMode"
            PG_COLOUR_ALLOW_CUSTOM            = u"AllowCustom"
            PG_COLOUR_HAS_ALPHA               = u"HasAlpha"

            NullProperty                      = None
            PGChoicesEmptyData                = None
            """)


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

