//--------------------------------------------------------------------------
// Name:        src/wxpybuffer.h
// Purpose:     A simple class to hold a pointer and a size.  See
//              wxpybuffer.sip for code that converts from a Python buffer
//              object as a MappedType.
//
// Author:      Robin Dunn
//
// Created:     26-Apr-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef WXPYBUFFER_H
#define WXPYBUFFER_H

// TODO: When support for Python2 is dropped then look into changing this
// class such that it holds on to the Py_buffer view object for the lifetime of
// the wxPyBuffer object. This could help with cases where the buffer is
// attempted to be accessed when the source object has already been gc'd.

class wxPyBuffer
{
public:
    wxPyBuffer() : m_ptr(NULL), m_len(0) {}

    // Initialize this object's pointer and length from a PyObject supporting
    // the Python buffer protocol.  Raises a TypeError if the object can not
    // be used as a buffer.
    bool create(PyObject* obj) {
        #if PY_MAJOR_VERSION < 3
            // Old buffer protocol
            int rv = PyObject_AsReadBuffer(obj, (const void**)&m_ptr, &m_len);
            if (rv != -1)
                return true;
        #endif
            // New buffer protocol
            Py_buffer view;
            if (PyObject_GetBuffer(obj, &view, PyBUF_SIMPLE) != 0)
                return false;
            m_ptr = view.buf;
            m_len = view.len;
            PyBuffer_Release(&view);
            return true;
    }


    // Ensure that the buffer's size is the expected size.  Raises a
    // Python ValueError exception and returns false if not.
    bool checkSize(Py_ssize_t expectedSize) {
        if (m_len < expectedSize) {
            wxPyErr_SetString(PyExc_ValueError, "Invalid data buffer size.");
            return false;
        }
        return true;
    }

    // Make a simple C copy of the data buffer.  Malloc is used because
    // the wxAPIs this is used with will later free() the pointer.  Raises
    // a Python exception if there is an allocation error.
    void* copy() {
        void* ptr = malloc(m_len);
        if (ptr == NULL) {
            wxPyBLOCK_THREADS(PyErr_NoMemory());
            return NULL;
        }
        memcpy(ptr, m_ptr, m_len);
        return ptr;
    }

    void*       m_ptr;
    Py_ssize_t  m_len;
};

#endif
//--------------------------------------------------------------------------
