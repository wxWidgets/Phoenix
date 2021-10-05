//--------------------------------------------------------------------------
// Name:        src/dc_ex.h
// Purpose:     Functions that can quickly draw lists of items on a DC
//
// Author:      Robin Dunn
//
// Created:     18-Aug-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

typedef bool (*wxPyDrawListOp_t)(wxDC& dc, PyObject* coords);

PyObject* wxPyDrawXXXList(wxDC& dc, wxPyDrawListOp_t doDraw,
                          PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes);

bool wxPyDrawXXXPoint(wxDC& dc, PyObject* coords);
bool wxPyDrawXXXLine(wxDC& dc, PyObject* coords);
bool wxPyDrawXXXRectangle(wxDC& dc, PyObject* coords);
bool wxPyDrawXXXEllipse(wxDC& dc, PyObject* coords);
bool wxPyDrawXXXPolygon(wxDC& dc, PyObject* coords);

PyObject* wxPyDrawTextList(wxDC& dc, PyObject* textList, PyObject* pyPoints,
                           PyObject* foregroundList, PyObject* backgroundList);

//--------------------------------------------------------------------------


PyObject* wxPyDrawXXXList(wxDC& dc, wxPyDrawListOp_t doDraw,
                          PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)
{
    wxPyBlock_t blocked = wxPyBeginBlockThreads();

    bool      isFastSeq  = PyList_Check(pyCoords) || PyTuple_Check(pyCoords);
    bool      isFastPens = PyList_Check(pyPens) || PyTuple_Check(pyPens);
    bool      isFastBrushes = PyList_Check(pyBrushes) || PyTuple_Check(pyBrushes);
    int       numObjs = 0;
    int       numPens = 0;
    int       numBrushes = 0;
    wxPen*    pen;
    wxBrush*  brush;
    PyObject* obj;
    PyObject* coords;
    int       i = 0;
    PyObject* retval;

    if (!PySequence_Check(pyCoords)) {
        goto err0;
    }
    if (!PySequence_Check(pyPens)) {
        goto err1;
    }
    if (!PySequence_Check(pyBrushes)) {
        goto err2;
    }
    numObjs = PySequence_Length(pyCoords);
    numPens = PySequence_Length(pyPens);
    numBrushes = PySequence_Length(pyBrushes);
    for (i = 0; i < numObjs; i++) {
        // Use a new pen?
        if (i < numPens) {
            if (isFastPens) {
                obj = PySequence_Fast_GET_ITEM(pyPens, i);
            }
            else {
                obj = PySequence_GetItem(pyPens, i);
            }
            if (! wxPyConvertWrappedPtr(obj, (void **) &pen, "wxPen")) {
                if (!isFastPens)
                    Py_DECREF(obj);
                goto err1;
            }

            dc.SetPen(*pen);
            if (!isFastPens)
                Py_DECREF(obj);
        }
        // Use a new brush?
        if (i < numBrushes) {
            if (isFastBrushes) {
                obj = PySequence_Fast_GET_ITEM(pyBrushes, i);
            }
            else {
                obj = PySequence_GetItem(pyBrushes, i);
            }
            if (!wxPyConvertWrappedPtr(obj, (void **) &brush, "wxBrush")) {
                if (!isFastBrushes)
                    Py_DECREF(obj);
                goto err2;
            }

            dc.SetBrush(*brush);
            if (!isFastBrushes)
                Py_DECREF(obj);
        }

        // Get the Coordinates
        if (isFastSeq) {
            coords = PySequence_Fast_GET_ITEM(pyCoords, i);
        }
        else {
            coords = PySequence_GetItem(pyCoords, i);
        }


        // call the drawOp
        bool success = doDraw(dc, coords);
        if (!isFastSeq)
            Py_DECREF(coords);

        if (! success) {
            retval = NULL;
            goto exit;
        }

    } // end of main for loop

    Py_INCREF(Py_None);
    retval = Py_None;
    goto exit;


 err0:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of coordinates");
    retval = NULL;
    goto exit;

 err1:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of wxPens");
    retval = NULL;
    goto exit;

 err2:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of wxBrushes");
    retval = NULL;
    goto exit;


 exit:
    wxPyEndBlockThreads(blocked);
    return retval;
}



bool wxPyDrawXXXPoint(wxDC& dc, PyObject* coords)
{
    int x, y;

    if (! wxPy2int_seq_helper(coords, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of (x,y) sequences.");
        return false;
    }
    dc.DrawPoint(x, y);
    return true;
}

bool wxPyDrawXXXLine(wxDC& dc, PyObject* coords)
{
    int x1, y1, x2, y2;

    if (! wxPy4int_seq_helper(coords, &x1, &y1, &x2, &y2)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of (x1,y1, x1,y2) sequences.");
        return false;
    }
    dc.DrawLine(x1,y1, x2,y2);
    return true;
}

bool wxPyDrawXXXRectangle(wxDC& dc, PyObject* coords)
{
    int x, y, w, h;

    if (! wxPy4int_seq_helper(coords, &x, &y, &w, &h)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of (x,y, w,h) sequences.");
        return false;
    }
    dc.DrawRectangle(x, y, w, h);
    return true;
}

bool wxPyDrawXXXEllipse(wxDC& dc, PyObject* coords)
{
    int x, y, w, h;

    if (! wxPy4int_seq_helper(coords, &x, &y, &w, &h)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of (x,y, w,h) sequences.");
        return false;
    }
    dc.DrawEllipse(x, y, w, h);
    return true;
}


wxPoint* wxPoint_LIST_helper(PyObject* source, int *count);

bool wxPyDrawXXXPolygon(wxDC& dc, PyObject* coords)
{
    wxPoint* points;
    int numPoints;

    points = wxPoint_LIST_helper(coords, &numPoints);
    if (! points) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of sequences of (x,y) sequences.");
        return false;
    }
    dc.DrawPolygon(numPoints, points);
    delete [] points;
    return true;
}


//---------------------------------------------------------------------------



PyObject* wxPyDrawTextList(wxDC& dc, PyObject* textList, PyObject* pyPoints, PyObject* foregroundList, PyObject* backgroundList)
{
    wxPyBlock_t blocked = wxPyBeginBlockThreads();

    bool      isFastSeq  = PyList_Check(pyPoints) || PyTuple_Check(pyPoints);
    bool      isFastText = PyList_Check(textList) || PyTuple_Check(textList);
    bool      isFastForeground = PyList_Check(foregroundList) || PyTuple_Check(foregroundList);
    bool      isFastBackground = PyList_Check(backgroundList) || PyTuple_Check(backgroundList);
    int       numText = 0;
    int       numPoints = 0;
    int       numForeground = 0;
    int       numBackground = 0;
    PyObject* obj;
    int       x1, y1;
    int       i = 0;
    wxColor*    color;
    PyObject* retval;
    wxString  string;

    if (!PySequence_Check(pyPoints)) {
        goto err0;
    }
    if (!PySequence_Check(textList)) {
        goto err1;
    }
    if (!PySequence_Check(foregroundList)) {
        goto err2;
    }
    if (!PySequence_Check(backgroundList)) {
        goto err3;
    }
    numPoints = PySequence_Length(pyPoints);
    numText = PySequence_Length(textList);
    numForeground = PySequence_Length(foregroundList);
    numBackground = PySequence_Length(backgroundList);

    for (i = 0; i < numPoints; i++) {
        // Use a new string ?
        if (i < numText) {
            if ( isFastText ) {
                obj = PySequence_Fast_GET_ITEM(textList, i);
            }
            else {
                obj = PySequence_GetItem(textList, i);
            }
            if (! PyBytes_Check(obj) && !PyUnicode_Check(obj) ) {
                Py_DECREF(obj);
                goto err1;
            }
            string = Py2wxString(obj);
            if ( !isFastText )
                Py_DECREF(obj);
        }

        if (i < numForeground) {
            // Use a new foreground ?
            if ( isFastForeground ) {
                obj = PySequence_Fast_GET_ITEM(foregroundList, i);
            }
            else {
                obj = PySequence_GetItem(foregroundList, i);
            }
            if (! wxPyConvertWrappedPtr(obj, (void **) &color, "wxColour")) {
                if (!isFastForeground)
                    Py_DECREF(obj);
                goto err2;
            }
            dc.SetTextForeground(*color);
            if ( !isFastForeground )
                Py_DECREF(obj);
        }

        if (i < numBackground) {
            // Use a new background ?
            if ( isFastBackground ) {
                obj = PySequence_Fast_GET_ITEM(backgroundList, i);
            }
            else {
                obj = PySequence_GetItem(backgroundList, i);
            }
            if (! wxPyConvertWrappedPtr(obj, (void **) &color, "wxColour")) {
                if (!isFastBackground)
                    Py_DECREF(obj);
                goto err3;
            }
            dc.SetTextBackground(*color);
            if ( !isFastBackground )
                Py_DECREF(obj);
        }

        // Get the point coordinates
        if (isFastSeq) {
            obj = PySequence_Fast_GET_ITEM(pyPoints, i);
        }
        else {
            obj = PySequence_GetItem(pyPoints, i);
        }
        if (! wxPy2int_seq_helper(obj, &x1, &y1)) {
            if (! isFastSeq)
                Py_DECREF(obj);
            goto err0;
        }
        if (!isFastText)
            Py_DECREF(obj);

        if (PyErr_Occurred()) {
            retval = NULL;
            goto exit;
        }

        // Now draw the text
        dc.DrawText(string, x1, y1);
    }

    Py_INCREF(Py_None);
    retval = Py_None;
    goto exit;

 err0:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of (x,y) sequences.");
    retval = NULL;
    goto exit;
 err1:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of strings");
    retval = NULL;
    goto exit;

 err2:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of wxColours for foregrounds");
    retval = NULL;
    goto exit;

 err3:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of wxColours for backgrounds");
    retval = NULL;
    goto exit;

 exit:
    wxPyEndBlockThreads(blocked);
    return retval;
}

//---------------------------------------------------------------------------


bool wxPointFromObjects(PyObject* o1, PyObject* o2, wxPoint* point)
{
    // get the x value
    if (wxPyInt_Check(o1))
        point->x = (int)wxPyInt_AS_LONG(o1);
    else if (PyFloat_Check(o1))
        point->x = (int)PyFloat_AS_DOUBLE(o1);
    else if (PyNumber_Check(o1))
        point->x = (int)wxPyInt_AsLong(o1);
    else
        return false;

    // get the y value
    if (wxPyInt_Check(o2))
        point->y = (int)wxPyInt_AS_LONG(o2);
    else if (PyFloat_Check(o2))
        point->y = (int)PyFloat_AS_DOUBLE(o2);
    else if (PyNumber_Check(o2))
        point->y = (int)wxPyInt_AsLong(o2);
    else
        return false;

    return true;
}


wxPoint* wxPoint_LIST_helper(PyObject* source, int *count)
{
    int idx;
    wxPoint* temp;
    PyObject *o, *o1, *o2;
    bool isFast = PyList_Check(source) || PyTuple_Check(source);

    if (!PySequence_Check(source)) {
        goto error0;
    }

    // The length of the sequence is returned in count.
    *count = PySequence_Length(source);
    if (*count < 0) {
        goto error0;
    }

    temp = new wxPoint[*count];
    if (!temp) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate temporary array");
        return NULL;
    }
    for (idx=0; idx<*count; idx++) {
        // Get an item: try fast way first.
        if (isFast) {
            o = PySequence_Fast_GET_ITEM(source, idx);
        }
        else {
            o = PySequence_GetItem(source, idx);
            if (o == NULL) {
                goto error1;
            }
        }

        // Convert o to wxPoint.
        if ((PyTuple_Check(o) && PyTuple_GET_SIZE(o) == 2) ||
            (PyList_Check(o) && PyList_GET_SIZE(o) == 2)) {
            o1 = PySequence_Fast_GET_ITEM(o, 0);
            o2 = PySequence_Fast_GET_ITEM(o, 1);
            if (!wxPointFromObjects(o1, o2, &temp[idx])) {
                goto error2;
            }
        }
        else if (wxPyWrappedPtr_Check(o)) {
            wxPoint* pt;
            if (! wxPyConvertWrappedPtr(o, (void **)&pt, "wxPoint")) {
                goto error2;
            }
            temp[idx] = *pt;
        }
        else if (PySequence_Check(o) && PySequence_Length(o) == 2) {
            o1 = PySequence_GetItem(o, 0);
            o2 = PySequence_GetItem(o, 1);
            if (!wxPointFromObjects(o1, o2, &temp[idx])) {
                goto error3;
            }
            Py_DECREF(o1);
            Py_DECREF(o2);
        }
        else {
            goto error2;
        }
        // Clean up.
        if (!isFast)
            Py_DECREF(o);
    }
    return temp;

error3:
    Py_DECREF(o1);
    Py_DECREF(o2);
error2:
    if (!isFast)
        Py_DECREF(o);
error1:
    delete [] temp;
error0:
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of length-2 sequences or wx.Points.");
    return NULL;
}


PyObject* wxPyDrawLinesFromBuffer(wxDC& dc, PyObject* pyBuff)
{
    wxPyBlock_t blocked = wxPyBeginBlockThreads();
    Py_buffer view;
    PyObject* retval;


    if (!PyObject_CheckBuffer(pyBuff)) {
        goto err0;
    }
    
    if (PyObject_GetBuffer(pyBuff, &view, PyBUF_CONTIG) < 0) {
        goto err1;
    }
    
    if (view.itemsize * 2 != sizeof(wxPoint)) {
        goto err2;
    }
    
    dc.DrawLines(view.len / view.itemsize / 2, (wxPoint *)view.buf);
    
    PyBuffer_Release(&view);

    Py_INCREF(Py_None);
    retval = Py_None;
    goto exit;


 err0:
    PyErr_SetString(PyExc_TypeError, "Expected a buffer object");
    retval = NULL;
    goto exit;
    
 err1:
    // PyObject_GetBuffer raises exception already
    retval = NULL;
    goto exit;

 err2:
    PyErr_SetString(PyExc_TypeError, "Item size does not match wxPoint size");
    retval = NULL;
    goto exit;

 exit:
    wxPyEndBlockThreads(blocked);
    return retval;
}

