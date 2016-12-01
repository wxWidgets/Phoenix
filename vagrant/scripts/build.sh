#!/bin/bash
#--------------------------------------------------------------------------
# This script is run in the Vagrant VMs and performs the actual build of
# Phoenix.  It expects to find a source tarball in ../../dist, (which is
# mapped to ~/dist in the VM) and to be given a name on the command-line to
# be used to distinguish this build from the other linux builds.
#--------------------------------------------------------------------------

set -o errexit

NAME=$1
if [ "$NAME" == "" ]; then
    echo "ERROR: Build name must be given on the command line."
    exit 1
fi

PYVER=$2
if [ "$PYVER" == "" ]; then
    PYVER=all
fi

PORT=$3
if [ "$PORT" == "" ]; then
    PORT=all
fi


TARBALL=$(ls ~/dist/wxPython_Phoenix-*.tar.gz)
if [ "$TARBALL" == "" ]; then
    echo "ERROR: Source tarball not found."
    exit 1
fi



# This function is called to do each build.
# It is given the virtual environment to be used, a tag (gtk2 or gtk3) to be
# used to help name the target folder, and an optional flag (--gtk3) to be
# passed on the build.py command line.
function do_build {
    VENV=$1
    TAG=$2
    FLAG=$3

    # setup
    echo "**** do_build ****"
    echo "Using Python from VENV $VENV"
    ORIG_PATH=$PATH
    export PATH=$VENV/bin:$PATH
    echo PYTHON: $(which python)
    echo $(python -c "import sys; print(sys.version)")

    # move into the source tree
    cd ~/wxPython_Phoenix-*

    # update packages
    pip install -U pip
    pip install -U -r requirements.txt

    # Build wxWidgets, Phoenix and a Wheel
    # Since we're using a source tarball we don't need to do all the code
    # generation parts, all files should already be present
    python build.py $FLAG build_wx build_py bdist_wheel

    # copy the results back to the host shared dist folder
    mkdir -p ~/dist/$NAME/$TAG
    mv dist/*.whl ~/dist/$NAME/$TAG

    # clean up
    python build.py clean
    rm -rf dist build
    export PATH=$ORIG_PATH
}


# Get things started...
echo "Unpacking source archive..."
tar xzf $TARBALL


# Do a build for each Python virtual environment in ~/venvs
for VENV in ~/venvs/*; do

    if [ $PYVER = all -o $PYVER = $(basename $VENV) ]; then
        # build a package for GTK2?
        if [ $PORT = all -o $PORT = gtk2 ]; then
            do_build $VENV gtk2
        fi

        # build a package for GTK3?
        if [ $PORT = all -o $PORT = gtk3 ]; then
            do_build $VENV gtk3 --gtk3
        fi
    fi
done

rm -r ~/wxPython_Phoenix-*
