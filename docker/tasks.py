#!/usr/bin/python
#----------------------------------------------------------------------
# Name:        tasks.py
# Purpose:     Invoke-based set of commands for dealing with wxPython's
#              Docker files, images and performing wxPython builds.
#
# Author:      Robin Dunn
#
# Created:     1-July-2019
# Copyright:   (c) 2019 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import os
import glob
from invoke import task, run


HERE = os.path.abspath(os.path.dirname(__file__))


@task(
    help={'upload':'Upload the resulting images to docker hub',
          'image':'Name of a docker image to build. May be specified more than once. Defaults to all.',
          },
    iterable=['image'],
)
def build_images(ctx, image, upload=False ):
    """
    Build the docker images.
    """
    if image == []:
        image = _get_all_distros()

    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    for img_name in image:
        # build it
        ctx.run('docker build --no-cache '
                '-f {name}/Dockerfile '
                '-t wxpython/build:{name}  .'.format(name=img_name),
                pty=True, echo=True)
        # test it
        ctx.run('docker run -it --rm -v {}:/dist '
                'wxpython/build:{} hello.sh'.format(dist, img_name),
                pty=True, echo=True)

    if upload:
        print('Do image upload here...')


@task(
    help={
        'image':'Name of a docker image to use for building. May be specified more than once. Defaults to all.',
        'port': 'One of gtk2, gtk3 or all. Defaults to all.',
        'venv': 'The name of a Python virtual environment to use for the build, like Py27, Py36, etc. Defaults to all.'
    },
    iterable=['image'],
)
def build_wxpython(ctx, image, venv='all', port='all', upload=False, release=False):
    """
    Use docker images to build wxPython.

    This command requires that there is a wxPython source archive in the ../dist
    folder, such as one produced by `python build.py sdist` or one from a
    release or snapshot build of wxPython.
    """
    if image == []:
        image = _get_all_distros()

    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    for img_name in image:
        ctx.run('docker run -it --rm -v {}:/dist '
                'wxpython/build:{} do-build.sh {} {}'.format(dist, img_name, venv, port),
                pty=True, echo=True)


def _get_all_distros():
    os.chdir(HERE)
    all_matching = glob.glob("*-*")
    return all_matching
