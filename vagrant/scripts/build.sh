#!/bin/bash
#--------------------------------------------------------------------------
# This script is run in the Vagrant VMs and performs the actual build of
# Phoenix.  It expects to find a source tarball in ../../dist, (which is
# mapped to ~/dist in the VM) and to be given a name on the command-line to
# be used to distinguish this build from the other linux builds.
#--------------------------------------------------------------------------


NAME=$1
if [ "$NAME" == "" ]; then
    echo "ERROR: Build name must be given on the command line."
    exit 1
fi

TARBALL=$(ls ~/dist/wxPython_Phoenix-*.tar.gz)
if [ "$TARBALL" == "" ]; then
    echo "ERROR: Source tarball not found."
    exit 1
fi

echo "Unpacking source archive..."
tar xzf $TARBALL

# Do a build for each Python virtual environment in ~/venvs
for VENV in ~/venvs/*; do

    # setup
    echo "Activating $VENV"
    source $VENV/bin/activate

    pushd ~/wxPython_Phoenix-*

    # update packages
    pip install -U pip
    pip install -U -r requirements.txt

    # build with gtk2
    rm -rf dist
    python build.py build
    python build.py bdist_wheel
    mkdir -p ~/dist/$NAME
    mv dist/*.whl ~/dist/$NAME
    python build.py clean

    # Now do the same for a gtk3 build
    rm -rf dist
    python build.py build --gtk3
    python build.py bdist_wheel
    mkdir -p ~/dist/$NAME-gtk3
    mv dist/*.whl ~/dist/$NAME-gtk3
    python build.py clean

    deactivate
    popd
done

rm -r ~/wxPython_Phoenix-*
