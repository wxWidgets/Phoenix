#---------------------------------------------------------------------------
# Name:        etg/joystick.py
# Author:      Robin Dunn
#
# Created:     19-May-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "joystick"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxJoystick",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("""\
        #if !wxUSE_JOYSTICK && !defined(__WXMSW__)
        // A C++ stub class for wxJoystick for platforms that don't have it.
        class wxJoystick : public wxObject {
        public:
            wxJoystick(int joystick = wxJOYSTICK1) {
                wxPyErr_SetString(PyExc_NotImplementedError,
                                  "wxJoystick is not available on this platform.");
            }
            wxPoint GetPosition() const { return wxPoint(-1,-1); }
            int GetPosition(unsigned axis) const { return -1; }
            int GetZPosition() const { return -1; }
            int GetButtonState() const { return -1; }
            int GetButtonState(unsigned button) const { return -1; }
            int GetPOVPosition() const { return -1; }
            int GetPOVCTSPosition() const { return -1; }
            int GetRudderPosition() const { return -1; }
            int GetUPosition() const { return -1; }
            int GetVPosition() const { return -1; }
            int GetMovementThreshold() const { return -1; }
            void SetMovementThreshold(int threshold) {}

            bool IsOk(void) const { return false; }
            static int GetNumberJoysticks() { return -1; }
            int GetManufacturerId() const { return -1; }
            int GetProductId() const { return -1; }
            wxString GetProductName() const { return wxEmptyString; }
            int GetXMin() const { return -1; }
            int GetYMin() const { return -1; }
            int GetZMin() const { return -1; }
            int GetXMax() const { return -1; }
            int GetYMax() const { return -1; }
            int GetZMax() const { return -1; }
            int GetNumberButtons() const { return -1; }
            int GetNumberAxes() const { return -1; }
            int GetMaxButtons() const { return -1; }
            int GetMaxAxes() const { return -1; }
            int GetPollingMin() const { return -1; }
            int GetPollingMax() const { return -1; }
            int GetRudderMin() const { return -1; }
            int GetRudderMax() const { return -1; }
            int GetUMin() const { return -1; }
            int GetUMax() const { return -1; }
            int GetVMin() const { return -1; }
            int GetVMax() const { return -1; }

            bool HasRudder() const { return false; }
            bool HasZ() const { return false; }
            bool HasU() const { return false; }
            bool HasV() const { return false; }
            bool HasPOV() const { return false; }
            bool HasPOV4Dir() const { return false; }
            bool HasPOVCTS() const { return false; }

            bool SetCapture(wxWindow* win, int pollingFreq = 0) { return false; }
            bool ReleaseCapture() { return false; }
        };
        #endif
        """)


    c = module.find('wxJoystick')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

