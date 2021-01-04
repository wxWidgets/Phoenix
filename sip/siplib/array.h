/*
 * This file defines the API for the array type.
 *
 * Copyright (c) 2019 Riverbank Computing Limited <info@riverbankcomputing.com>
 *
 * This file is part of SIP.
 *
 * This copy of SIP is licensed for use under the terms of the SIP License
 * Agreement.  See the file LICENSE for more details.
 *
 * This copy of SIP may also used under the terms of the GNU General Public
 * License v2 or v3 as published by the Free Software Foundation which can be
 * found in the files LICENSE-GPL2 and LICENSE-GPL3 included in this package.
 *
 * SIP is supplied WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */


#ifndef _ARRAY_H
#define _ARRAY_H


#include <Python.h>

#include "sipint.h"


#ifdef __cplusplus
extern "C" {
#endif


extern PyTypeObject sipArray_Type;

PyObject *sip_api_convert_to_array(void *data, const char *format,
        Py_ssize_t len, int flags);
PyObject *sip_api_convert_to_typed_array(void *data, const sipTypeDef *td,
        const char *format, size_t stride, Py_ssize_t len, int flags);


#ifdef __cplusplus
}
#endif

#endif
