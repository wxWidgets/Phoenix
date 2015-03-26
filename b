#!/bin/bash

##set -o xtrace

#PYVER=2.7
#PYVER2=27
PYVER=3.4
PYVER2=34

if [ "$OSTYPE" = "cygwin" ]; then
    $TOOLS/python$PYVER2/python.exe -u build.py "$@"
else
    PATH=/usr/local/bin:$PATH
    PYTHON=`which python$PYVER`
    $PYTHON -u build.py "$@"
fi

exit $?
