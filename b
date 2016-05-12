#!/bin/bash

##set -o xtrace

if [ "$OSTYPE" = "cygwin" ]; then
    PYTHON=`which python.exe`
    echo $PYTHON
    $PYTHON -u build.py "$@"
else
    PYTHON=`which python`
    echo $PYTHON
    $PYTHON -u build.py "$@"
fi

exit $?
