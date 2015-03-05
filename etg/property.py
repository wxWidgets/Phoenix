#---------------------------------------------------------------------------
# Name:        etg/property.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_propgrid"
NAME      = "property"   # Base name of the file to generate to for this script
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


    c = module.find('wxPGAttributeStorage')
    # TODO: Add methods to add a Python iterator using these methods
    c.find('StartIteration').ignore()
    c.find('GetNext').ignore()
    c.find('const_iterator').ignore()


    c = module.find('wxPGProperty')
    tools.ignoreConstOverloads(c)


    c = module.find('wxPGChoicesData')
    tools.ignoreConstOverloads(c)
    #c.addDtor() 
    c.find('~wxPGChoicesData').ignore(False)


    c = module.find('wxPGChoices')
    c.find('wxPGChoices').findOverload('wxChar **').ignore()
    tools.ignoreConstOverloads(c)

    # Ignore some string constants (#defines) coming from dox, and add them
    # back in Python code. They are wchar_t* values and this seened the
    # simplest way to deal with them.
    for name in [ 'wxPG_ATTR_DEFAULT_VALUE',
                  'wxPG_ATTR_MIN',
                  'wxPG_ATTR_MAX',
                  'wxPG_ATTR_UNITS',
                  'wxPG_ATTR_HINT',
                  'wxPG_ATTR_INLINE_HELP',
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
                  'wxPG_FILE_DIALOG_TITLE',
                  'wxPG_FILE_DIALOG_STYLE',
                  'wxPG_DIR_DIALOG_MESSAGE',
                  'wxPG_ARRAY_DELIMITER',
                  'wxPG_DATE_FORMAT',
                  'wxPG_DATE_PICKER_STYLE',
                  'wxPG_ATTR_SPINCTRL_STEP',
                  'wxPG_ATTR_SPINCTRL_WRAP',
                  'wxPG_ATTR_SPINCTRL_MOTIONSPIN',
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
            PG_ATTR_INLINE_HELP               = u"InlineHelp"
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
            PG_FILE_DIALOG_STYLE              = u"DialogStyle"
            PG_DIR_DIALOG_MESSAGE             = u"DialogMessage"
            PG_ARRAY_DELIMITER                = u"Delimiter"
            PG_DATE_FORMAT                    = u"DateFormat"
            PG_DATE_PICKER_STYLE              = u"PickerStyle"
            PG_ATTR_SPINCTRL_STEP             = u"Step"
            PG_ATTR_SPINCTRL_WRAP             = u"Wrap"
            PG_ATTR_SPINCTRL_MOTIONSPIN       = u"MotionSpin"
            PG_ATTR_MULTICHOICE_USERSTRINGMODE= u"UserStringMode"
            PG_COLOUR_ALLOW_CUSTOM            = u"AllowCustom"
            PG_COLOUR_HAS_ALPHA               = u"HasAlpha"

            NullProperty                      = None
            PGChoicesEmptyData                = None
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

