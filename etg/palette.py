#---------------------------------------------------------------------------
# Name:        etg/palette.py
# Author:      Scott Talbert
#
# Created:     31-Jul-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from textwrap import dedent

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "palette"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPalette' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    c = module.find('wxPalette')
    tools.removeVirtuals(c)


    # Add a helper function for use with the Create method and the Ctor
    # accepting RGB data.
    c.addCppCode("""\
        // a helper function to be used in the Create method and one of the Ctors
        bool _paletteCreateHelper(wxPalette* self,
                                  PyObject* red, PyObject* green, PyObject* blue) {
            bool rval = false;
            wxPyThreadBlocker blocker;
            char* errMsg = "Expected a sequence of integer objects";

            if (!PySequence_Check(red) || !PySequence_Check(green) || !PySequence_Check(blue)) {
                PyErr_SetString(PyExc_TypeError, errMsg);
                return rval;
            }

            Py_ssize_t count = PySequence_Size(red);
            if (PySequence_Size(green) != count || PySequence_Size(blue) != count) {
                PyErr_SetString(PyExc_ValueError, "Sequence lengths must be equal");
                return rval;
            }

            unsigned char* redArray = new unsigned char[count];
            unsigned char* greenArray = new unsigned char[count];
            unsigned char* blueArray = new unsigned char[count];

            for (Py_ssize_t i = 0; i < count; i++) {
                PyObject* redItem = PySequence_ITEM(red, i);
                PyObject* greenItem = PySequence_ITEM(green, i);
                PyObject* blueItem = PySequence_ITEM(blue, i);
                if (!wxPyInt_Check(redItem) || !wxPyInt_Check(greenItem) || !wxPyInt_Check(blueItem)) {
                    PyErr_SetString(PyExc_TypeError, errMsg);
                    goto pch_exit;
                }

                long redLong = wxPyInt_AsLong(redItem);
                long greenLong = wxPyInt_AsLong(greenItem);
                long blueLong = wxPyInt_AsLong(blueItem);
                Py_DECREF(redItem);
                Py_DECREF(greenItem);
                Py_DECREF(blueItem);
                if (redLong < 0 || redLong > 255 || greenLong < 0 || greenLong > 255 || blueLong < 0 || blueLong > 255) {
                    PyErr_SetString(PyExc_ValueError, "Sequence values must be in the 0..255 range");
                    goto pch_exit;
                }
                redArray[i] = redLong;
                greenArray[i] = greenLong;
                blueArray[i] = blueLong;
            }

            rval = self->Create(count, redArray, greenArray, blueArray);

        pch_exit:
            delete[] redArray;
            delete[] greenArray;
            delete[] blueArray;
            return rval;
        }
        """)


    #-----------------------------------------------------------------

    # Replace the constructor accepting the arrays of RGB values with one that
    # understands any Python sequence.
    c.find('wxPalette').findOverload('red').ignore()
    c.addCppCtor('(PyObject* red, PyObject* green, PyObject* blue)',
        doc=dedent("""\
        Creates a palette from a set of sequences of integers,
        one for each red, green and blue color components.

        :param red: A sequence of integer values in the range 0..255 inclusive.
        :param green: A sequence of integer values in the range 0..255 inclusive.
        :param blue: A sequence of integer values in the range 0..255 inclusive.

        .. note:: All sequences must be the same length.
        """),
        body="""\
            wxPalette* pal = new wxPalette;
            _paletteCreateHelper(pal, red, green, blue);
            if (PyErr_Occurred()) {
                delete pal;
                return NULL;
            }
            return pal;
            """)

    c.find('GetPixel.red').pyInt = True
    c.find('GetPixel.green').pyInt = True
    c.find('GetPixel.blue').pyInt = True

    c.find('GetRGB').ignore()
    c.addCppMethod('PyObject*', 'GetRGB', '(int pixel)',
        pyArgsString="(pixel) -> (red, green, blue)",
        doc="Returns RGB values for a given palette index.",
        body="""\
            unsigned char red;
            unsigned char green;
            unsigned char blue;
            wxPyThreadBlocker blocker;
            if (!self->GetRGB(pixel, &red, &green, &blue)) {
                PyErr_SetString(PyExc_IndexError, "Pixel out of range");
                return NULL;
            }
            PyObject* rv = PyTuple_New(3);
            PyTuple_SetItem(rv, 0, wxPyInt_FromLong(red));
            PyTuple_SetItem(rv, 1, wxPyInt_FromLong(green));
            PyTuple_SetItem(rv, 2, wxPyInt_FromLong(blue));
            return rv;
            """)

    # Replace the Create method with one that understands any kind of Python sequence
    c.find('Create').ignore()
    c.addCppMethod('PyObject*', 'Create', '(PyObject* red, PyObject* green, PyObject* blue)',
        pyArgsString="(red, green, blue) -> bool",
        doc=dedent("""\
        Creates a palette from 3 sequences of integers, one for each red, blue or green component.

        :param red: A sequence of integer values in the range 0..255 inclusive.
        :param green: A sequence of integer values in the range 0..255 inclusive.
        :param blue: A sequence of integer values in the range 0..255 inclusive.

        .. note:: All sequences must be the same length.
        """),
        body="""\
            bool rval = _paletteCreateHelper(self, red, green, blue);
            wxPyThreadBlocker blocker;
            if (PyErr_Occurred())
                return NULL;
            if (rval)
                Py_RETURN_TRUE;
            else
                Py_RETURN_FALSE;
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
