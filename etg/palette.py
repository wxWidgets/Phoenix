#---------------------------------------------------------------------------
# Name:        etg/palette.py
# Author:      Scott Talbert
#
# Created:     31-Jul-2016
# Copyright:   (c) 2016 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

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


    c.find('GetPixel.red').pyInt = True
    c.find('GetPixel.green').pyInt = True
    c.find('GetPixel.blue').pyInt = True

    c.find('GetRGB').ignore()
    c.addCppMethod('PyObject*', 'GetRGB', '(int pixel)',
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

    c.find('Create').ignore()
    c.addCppMethod('PyObject*', 'Create', '(PyObject* red, PyObject* green, PyObject* blue)',
        doc="Creates a palette from 3 sequences of integers, one for each red, blue or green component.",
        body="""\
            wxPyThreadBlocker blocker;
            PyObject* rval;

            char* errMsg = "Expected a sequence of integer objects";
            if (!PySequence_Check(red) || !PySequence_Check(green) || !PySequence_Check(blue)) {
                PyErr_SetString(PyExc_TypeError, errMsg);
                return NULL;
            }

            Py_ssize_t count = PySequence_Size(red);
            if (PySequence_Size(green) != count || PySequence_Size(blue) != count) {
                PyErr_SetString(PyExc_ValueError, "Sequence lengths must be equal");
                return NULL;
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
                    rval = NULL;
                    goto exit;
                }

                long redLong = wxPyInt_AsLong(redItem);
                long greenLong = wxPyInt_AsLong(greenItem);
                long blueLong = wxPyInt_AsLong(blueItem);
                Py_DECREF(redItem);
                Py_DECREF(greenItem);
                Py_DECREF(blueItem);
                if (redLong < 0 || redLong > 255 || greenLong < 0 || greenLong > 255 || blueLong < 0 || blueLong > 255) {
                    PyErr_SetString(PyExc_ValueError, "Sequence values must be >= 0 and < 256");
                    rval = NULL;
                    goto exit;
                }
                redArray[i] = redLong;
                greenArray[i] = greenLong;
                blueArray[i] = blueLong;
            }

            if (self->Create(count, redArray, greenArray, blueArray)) {
                rval = Py_True;
                Py_INCREF(rval);
            } else {
                rval = Py_False;
                Py_INCREF(rval);
            }

            exit:
                delete[] redArray;
                delete[] greenArray;
                delete[] blueArray;
                return rval;
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
