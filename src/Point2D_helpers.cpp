
#define sipType_wxPoint2D   sipType_wxPoint2DDouble

// Convert a Python sequence of 2-tuples of numbers or wx.Point2D objects into a 
// C array of wxPoint2D instances
static
wxPoint2D* wxPoint2D_array_helper(PyObject* source, size_t *count)
{
    wxPoint2D* array;
    Py_ssize_t idx, len;
    
    // ensure that it is a sequence
    if (! PySequence_Check(source)) 
        goto error0;
    // ensure it is not a string or unicode object (they are sequences too)
    else if (PyString_Check(source) || PyUnicode_Check(source))
        goto error0;
    // ensure each item can be converted to wxPoint2D
    else {
        len = PySequence_Length(source);
        for (idx=0; idx<len; idx++) {
            PyObject* item = PySequence_ITEM(source, idx);
            if (!sipCanConvertToType(item, sipType_wxPoint2D, SIP_NOT_NONE)) {
                Py_DECREF(item);
                goto error0;
            }
            Py_DECREF(item);
        }    
    }
    
    // The length of the sequence is returned in count.
    *count = len;
    array = new wxPoint2D[*count];
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate temporary array");
        return NULL;
    }
    for (idx=0; idx<len; idx++) {
        PyObject* obj = PySequence_ITEM(source, idx);
        int state = 0;
        int err = 0;
        wxPoint2D* item = reinterpret_cast<wxPoint2D*>(
                        sipConvertToType(obj, sipType_wxPoint2D, NULL, 0, &state, &err));
        array[idx] = *item;
        sipReleaseType((void*)item, sipType_wxPoint2D, state); // delete temporary instances
        Py_DECREF(obj);
    }
    return array;

error0:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of length-2 sequences or wxPoint2D objects.");
    return NULL;
}
