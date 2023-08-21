#---------------------------------------------------------------------------
# Name:        etg/bmpbndl.py
# Author:      Scott Talbert
#
# Created:     13-Apr-2022
# Copyright:   (c) 2022 by Scott Talbert
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import MethodDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "bmpbndl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxBitmapBundle',
           'wxBitmapBundleImpl',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    #module.addHeaderCode('#include <wx/some_header_file.h>')

    c = module.find('wxBitmapBundle')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxBitmapBundle').findOverload('xpm').ignore()
    c.find('FromSVG').findOverload('char *data, const wxSize &sizeDef').ignore()
    c.find('FromImpl.impl').transfer = True

    # Allow on-the-fly creation of a wx.BitmapBundle from a wx.Bitmap, wx.Icon
    # or a wx.Image
    c.convertFromPyObject = """\
        // Check for type compatibility
        if (!sipIsErr) {
            if (sipCanConvertToType(sipPy, sipType_wxBitmap, SIP_NO_CONVERTORS))
                return 1;
            if (sipCanConvertToType(sipPy, sipType_wxIcon, SIP_NO_CONVERTORS))
                return 1;
            if (sipCanConvertToType(sipPy, sipType_wxImage, SIP_NO_CONVERTORS))
                return 1;
            if (sipCanConvertToType(sipPy, sipType_wxBitmapBundle, SIP_NO_CONVERTORS))
                return 1;
            return 0;
        }

        // Otherwise, a conversion is needed
        int state = 0;
        // TODO: A macro for these nearly identical statements would be a good idea...
        if (sipCanConvertToType(sipPy, sipType_wxBitmap, SIP_NO_CONVERTORS)) {
            wxBitmap* obj = reinterpret_cast<wxBitmap*>(
                sipConvertToType(sipPy, sipType_wxBitmap, sipTransferObj, SIP_NO_CONVERTORS, &state, sipIsErr));
            *sipCppPtr = new wxBitmapBundle(*obj);
            sipReleaseType(obj, sipType_wxBitmap, state);
            return sipGetState(sipTransferObj);
        }
        if (sipCanConvertToType(sipPy, sipType_wxIcon, SIP_NO_CONVERTORS)) {
            wxIcon* obj = reinterpret_cast<wxIcon*>(
                sipConvertToType(sipPy, sipType_wxIcon, sipTransferObj, SIP_NO_CONVERTORS, &state, sipIsErr));
            *sipCppPtr = new wxBitmapBundle(*obj);
            sipReleaseType(obj, sipType_wxIcon, state);
            return sipGetState(sipTransferObj);
        }
        if (sipCanConvertToType(sipPy, sipType_wxImage, SIP_NO_CONVERTORS)) {
            wxImage* obj = reinterpret_cast<wxImage*>(
                sipConvertToType(sipPy, sipType_wxImage, sipTransferObj, SIP_NO_CONVERTORS, &state, sipIsErr));
            *sipCppPtr = new wxBitmapBundle(*obj);
            sipReleaseType(obj, sipType_wxImage, state);
            return sipGetState(sipTransferObj);
        }

        // The final option is that it is already a wxBitmapBundle, so just fetch the pointer and return
        *sipCppPtr = reinterpret_cast<wxBitmapBundle*>(
            sipConvertToType(sipPy, sipType_wxBitmapBundle, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0; // not a new instance
        """


    c = module.find('wxBitmapBundleImpl')
    assert isinstance(c, etgtools.ClassDef)

    m = MethodDef(name='~wxBitmapBundleImpl', isDtor=True, isVirtual=True, protection='protected')
    c.addItem(m)

    c.find('DoGetPreferredSize').ignore(False)
    c.find('GetIndexToUpscale').ignore(False)
    c.find('GetNextAvailableScale').ignore(False)
    c.find('GetNextAvailableScale.i').inOut = True
    c.find('GetNextAvailableScale.i').name = 'idx'

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

