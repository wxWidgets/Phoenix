#---------------------------------------------------------------------------
# Name:        etg/propgriddefs.py
# Author:      Robin Dunn
#
# Created:     14-Feb-2017
# Copyright:   (c) 2017-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgriddefs"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'propgriddefs_8h.xml',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    # Newer Doxygen versions only emit this duplicate typedef in propgrid.h.
    callback = module.findItem('wxPGSortCallback')
    if callback is not None:
        callback.ignore()

    module.addPyCode(
        code="""\
        PG_LABEL = "@!"
        PG_LABEL_STRING = PG_LABEL
        PG_NULL_BITMAP = wx.NullBitmap
        PG_COLOUR_BLACK = wx.BLACK
        PG_DEFAULT_IMAGE_SIZE = wx.Size(-1, -1)
        """,
        order=15)

    # wx declares these scoped enums as bit flags, but sip makes them IntEnums,
    # which reject combined values, such as the flags that C++ passes to a Python
    # override of ValueToString. sip's BaseType=IntFlag would need ABI 13.
    flagsCode = module.addPyCode(
        code="""\
        def _makeFlagsEnum(enumClass):
            def _missing_(cls, value):
                names = [m.name for m in cls if m.value and m.value & value == m.value]
                member = int.__new__(cls, value)
                member._name_ = '|'.join(names) or str(value)
                member._value_ = value
                return member
            enumClass._missing_ = classmethod(_missing_)
            enumClass.__or__ = lambda self, other: enumClass(int(self) | int(other))
            enumClass.__ror__ = enumClass.__or__

        for _flagsEnum in (PGFlags, PGPropertyValuesFlags, PGPropValFormatFlags,
                           PGSelectPropertyFlags, PGSetValueFlags,
                           PGSplitterPositionFlags, PGVFBFlags):
            _makeFlagsEnum(_flagsEnum)
        del _flagsEnum, _makeFlagsEnum
        """,
        order=15)
    flagsCode.piIgnored = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

