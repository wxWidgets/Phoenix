//--------------------------------------------------------------------------
// Name:        wxvector.sip
// Purpose:     MappedType for wxVector
//
// Author:      Scott Talbert
//
// Created:     14-Apr-2022
// Copyright:   (c) 2022 by Scott Talbert
// Licence:     wxWindows license
//--------------------------------------------------------------------------

template<_TYPE_>
%MappedType wxVector<_TYPE_>
{
    %ConvertFromTypeCode
        PyObject *l = PyList_New(sipCpp->size());

        if (!l)
            return 0;

        for (int i = 0; i < sipCpp->size(); ++i) {
            _TYPE_ *t = new _TYPE_(sipCpp->at(i));
            PyObject *tobj = sipConvertFromNewType(t, sipType__TYPE_,
                    sipTransferObj);

            if (!tobj) {
                delete t;
                Py_DECREF(l);

                return 0;
            }

            PyList_SetItem(l, i, tobj);
        }

        return l;
    %End

    %ConvertToTypeCode
        PyObject *iter = PyObject_GetIter(sipPy);

        if (!sipIsErr) {
            PyErr_Clear();
            Py_XDECREF(iter);

            return (iter
#if PY_MAJOR_VERSION < 3
                    && !PyString_Check(sipPy)
#endif
                    && !PyUnicode_Check(sipPy));
        }

        if (!iter) {
            *sipIsErr = 1;

            return 0;
        }

        wxVector<_TYPE_> *wv = new wxVector<_TYPE_>;

        for (Py_ssize_t i = 0; ; ++i) {
            PyErr_Clear();
            PyObject *itm = PyIter_Next(iter);

            if (!itm) {
                if (PyErr_Occurred()) {
                    delete wv;
                    Py_DECREF(iter);
                    *sipIsErr = 1;

                    return 0;
                }

                break;
            }

            int state;
            _TYPE_ *t = reinterpret_cast<_TYPE_ *>(
                    sipForceConvertToType(itm, sipType__TYPE_, sipTransferObj,
                            SIP_NOT_NONE, &state, sipIsErr));

            if (*sipIsErr) {
                PyErr_Format(PyExc_TypeError,
                        "index %zd has type '%s' but '_TYPE_' is expected", i,
                        sipPyTypeName(Py_TYPE(itm)));

                Py_DECREF(itm);
                delete wv;
                Py_DECREF(iter);

                return 0;
            }

            wv->push_back(*t);

            sipReleaseType(t, sipType__TYPE_, state);
            Py_DECREF(itm);
        }

        Py_DECREF(iter);
 
        *sipCppPtr = wv;
 
        return sipGetState(sipTransferObj);
    %End
};