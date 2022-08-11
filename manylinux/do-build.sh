#!/bin/bash
#--------------------------------------------------------------------------
# This script is run inside the manylinux Docker container to perform the
# actual build of the Phoenix wheels. See tasks.py and README.md for details.
#--------------------------------------------------------------------------
set -o errexit
set -o xtrace

export PYTHONUNBUFFERED=1

VERSION=$1
shift
PYTHONS="$@"
if [ -z $PYTHONS ]; then
    PYTHONS=3.8
fi

echo VERSION: $VERSION
echo PYTHONS: $PYTHONS


function do_setup() {
    # Install extra pacakges needed for the build
    echo Installing Linux packages...
    yum -y -q install \
        freeglut-devel \
        mesa-libGL-devel \
        mesa-libGLU-devel \
        gstreamer1-devel \
        gstreamer1-plugins-base-devel \
        gtk3-devel \
        libjpeg-devel \
        libnotify \
        libnotify-devel \
        libpng-devel \
        libSM-devel \
        libtiff-devel \
        libXtst-devel \
        SDL2-devel \
        webkit2gtk3-devel

    # Unpack the source archive
    mkdir /build
    cd /build
    tar xzf /dist/wxPython-$VERSION.tar.gz
}


function do_build() {
    # Remove the '.' from the version. IOW, 3.9 --> 39
    py=$(echo $1 | sed 's/\.//')
    cd /build/wxPython-$VERSION

    # There's something odd about how the Pythons are set up on this image,
    # and/or how virtual envs are created with these Pythons. When using a
    # virtual env the python-config tools give the wrong paths for includes,
    # libs, etc. Maybe it's too many layers of symlinks? Anyway, we need to use
    # the real python binary instead of a virual env for our build because waf
    # needs a working python-config.
    PYTHON=/opt/python/cp$py-*/bin/python
    OLD_PATH=$PATH
    export PATH=$(dirname $PYTHON):$PATH

    # build
    $PYTHON -m pip install -U -r requirements.txt
    $PYTHON -m pip install -U pip setuptools wheel
    $PYTHON build.py build_wx
    $PYTHON build.py build_py
    $PYTHON build.py bdist_wheel

    # do the manylinux magic
    auditwheel show dist/wxPython-$VERSION-*linux*.whl
    # auditwheel repair -w dist --strip dist/*.whl
    auditwheel repair -w dist  dist/*.whl

    # do a quickie smoke-test with a virtual env
    mkdir tmp
    $PYTHON -m venv tmp/test
    tmp/test/bin/pip install -U pip
    tmp/test/bin/pip install dist/wxPython-*manylinux*
    tmp/test/bin/python -c "import wx; print(wx.version())"
    rm -rf tmp

    # Save the manylinux wheel to the host folder
    mv dist/wxPython-*-manylinux*.whl /dist
    rm dist/wxPython-*.whl
    export PATH=$OLD_PATH
}



do_setup
for pyver in $PYTHONS; do
    do_build $pyver
done

if [ -n $INTERACTIVE ]; then
    exec /bin/bash -i
fi

