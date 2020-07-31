Building wxPython4 with Docker
==============================

Introduction
------------

Docker is a relatively lightweight system for deploying containers with a
specified set of software running within them. A Docker container is less than a
virtual machine, but more than a chroot, and will typically be much more
performant than a VM, (sub-second startup time, less resource hungry, etc.)
Typically they would be used for deploying "containerized applications", but a
docker image can easily be created with all that's needed for building software
too.

The files and folders in this subtree provide the Dockerfiles and scripts needed
to build the Docker images, as well as for using those images to build wxPython
wheels for various Linux distributions. A current set of images are available on
Docker Hub at https://hub.docker.com/r/wxpython4/build. There is an image there
tagged with the same names as those in the ./build folder. For example, as of
this writing you can pull images with these names and tags:

    wxpython4/build:centos-7
    wxpython4/build:debian-9
    wxpython4/build:debian-10
    wxpython4/build:fedora-29
    wxpython4/build:fedora-30
    wxpython4/build:fedora-31
    wxpython4/build:ubuntu-14.04
    wxpython4/build:ubuntu-16.04
    wxpython4/build:ubuntu-18.04
    wxpython4/build:ubuntu-20.04


Building Images
---------------

Since images are available on DockerHub there shouldn't be much need for
building them yourself, but just in case, here is how to do it. All images
can be built with a simple command like this::

    inv build-images

And one or more specific images can be built like this::

    inv build-images -i debian-10 -i ubuntu-18.04

The ``inv`` command comes from the ``invoke`` package, which can be downloaded
and installed from PyPI. It loads a set of tasks from the ``tasks.py`` file in
this folder, and provides a command line interface for running those tasks.


Building wxPython
-----------------

To perform a build there must be one (and only one) wxPython source tarball
located in the ``../dist`` folder. This source archive can either be generated
with the ``build.py dox etg sip sdist`` command, or it can be downloaded from a
wxPython release on PyPI, or it can come from the wxPython snapshots server for
prerelease versions of the software.

With that source archive in place then a build for a specific distro can be done
like this (see the paragraph about ``invoke`` above)::

    inv build-wxpython -i ubuntu-18.04

That will do a build for all Pythons that are set up in the image, and both gtk2
and gtk3 if the image supports gtk2 (some don't.) To narrow the build down to
just one Python and one port, a command like this can be used::

    inv build-wxpython -i ubuntu-18.04 -p gtk3 -v Py37

And a bare ``inv build-wxpython`` will cause a build to be done for all distros,
all supported Pythons, and all supported ports. This will take a little while to
accomplish. Go binge-watch something on Netflix while you're waiting...

When the build(s) are finished the results will be placed in the
``../dist/linux`` folder, using the same folder structure for distros and ports
as is used on https://extras.wxpython.org/wxPython4/extras/linux/

