#!/bin/bash

##set -o xtrace

if [ "$OSTYPE" = "cygwin" ]; then
    PYTHON=`which python.exe`
    echo $PYTHON
    $PYTHON -u build.py --dev "$@"
else
    PYTHON=`which python`
    echo $PYTHON
    $PYTHON -u build.py --dev "$@"
fi

exit $?
