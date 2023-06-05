#!/usr/bin/env python
#----------------------------------------------------------------------
# Name:        tasks.py
# Purpose:     Invoke-based set of commands for dealing with wxPython's
#              Docker files, images and performing wxPython builds.
#
# Author:      Robin Dunn
#
# Created:     1-July-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import os
import glob
from invoke import task, run


HERE = os.path.abspath(os.path.dirname(__file__))

# Distros that have been promoted to Emeritus status. They can still be selected
# manually, but will be excluded by default when selecting all images.
OLD = [ 'debian-9',
        'ubuntu-14.04',
        'ubuntu-16.04',
        'ubuntu-18.04',
        'fedora-29',
        'fedora-30',
        'fedora-31',
        'fedora-32',
        'fedora-33',
        'fedora-35',
        'fedora-36',
        'centos-7',
        'centos-8',
        ]



@task(
    aliases=['build_image', 'bi'],
    help={
        'image': 'Name of a docker image to build. May be specified more than once. Defaults to all.',
        'gui':   'Build the gui version of an image instead of just the build image.',
        'include_old': 'Include the "OLD" distros when selecting all.'
        },
    iterable=['image'],
)
def build_images(ctx, image, gui=False, include_old=False):
    """
    Build docker image(s).
    """
    if image == []:
        image = _get_all_distros(gui, include_old)

    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    img_type = 'gui' if gui else 'build'
    for img_name in image:
        # build it
        ctx.run('docker build --no-cache '
                '-f {type}/{name}/Dockerfile '
                '-t wxpython4/{type}:{name}  .'.format(name=img_name, type=img_type),
                pty=True, echo=True)
        # test it
        test_images(ctx, [img_name], gui)


@task(
    aliases=['test_image', 'ti'],
    help={
        'image': 'Name of a docker image to test. May be specified more than once. Defaults to all.',
        'gui':   'Test the gui version of an image instead of just the build image.',
        'include_old': 'Include the "OLD" distros when selecting all.'
        },
    iterable=['image'],
)
def test_images(ctx, image, gui=False, include_old=False):
    """
    Build docker image(s).
    """
    if image == []:
        image = _get_all_distros(gui, include_old)

    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    img_type = 'gui' if gui else 'build'
    for img_name in image:
        # test it
        ctx.run('docker run -it --rm -v {}:/dist '
                'wxpython4/{}:{} hello.sh'.format(dist, img_type, img_name),
                pty=True, echo=True)


@task(
    help={
        'image': 'Name of a docker image to push. May be specified more than once. Defaults to all.',
        'gui':   'Push the gui version of an image instead of just the build image.',
        'include_old': 'Include the "OLD" distros when selecting all.'
        },
    iterable=['image'],
)
def push(ctx, image, gui=False, include_old=False):
    """
    Push one or more images to docker hub. User should have already run
    a `docker login` command.
    """
    if image == []:
        image = _get_all_distros(gui, include_old)

    os.chdir(HERE)
    img_type = 'gui' if gui else 'build'
    for img_name in image:
        # build it
        ctx.run(
            'docker push wxpython4/{type}:{name}'.format(name=img_name, type=img_type),
            pty=True, echo=True)


@task(
    aliases=['build_wxp', 'bwxp'],
    help={
        'image':'Name of a docker image to use for building. May be specified more than once. Defaults to all.',
        'port': 'One of "gtk2", "gtk3" or "all". Defaults to "gtk3".',
        'venv': 'The name of a Python virtual environment to use for the build, like Py27, Py36, etc. Defaults to all.',
        'include_old': 'Include the "OLD" distros when selecting all.',
        'keep': "Keep the container when it exits. Otherwise it will be auto-removed."
    },
    iterable=['image'],
)
def build_wxpython(ctx, image, venv='all', port='gtk3', include_old=False, keep=False):
    """
    Use docker images to build wxPython.

    This command requires that there is a wxPython source archive in the ../dist
    folder, such as one produced by `python build.py sdist` or one from a
    release or snapshot build of wxPython.
    """
    if image == []:
        image = _get_all_distros(False, include_old)

    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    rm = '' if keep else '--rm'
    for img_name in image:
        ctx.run('docker run -it {} -v {}:/dist '
                'wxpython4/build:{} do-build.sh {} {}'.format(rm, dist, img_name, venv, port),
                pty=True, echo=True)


@task(
    help={
        'image_tag':"The tag of the image to be run",
        'cmd': "If given will run this command instead of the image's default command.",
        'gui': "If given will run the 'gui' image insead of the 'build' image.",
        'port': "Host port to use for the VNC connection.",
        'keep': "Keep the container when it exits. Otherwise it will be auto-removed."
    },
    positional=['image_tag'],
)
def run(ctx, image_tag, cmd=None, gui=False, port=5901, keep=False):
    """
    Run a wxpython docker image.
    """
    os.chdir(HERE)
    dist=os.path.abspath('../dist')
    imgtype = 'gui' if gui else 'build'
    cmd = '' if cmd is None else cmd
    rm = '' if keep else '--rm'
    ctx.run(
        'docker run -it {} -v {}:/dist -p {}:5901 wxpython4/{}:{} {}'.format(
            rm, dist, port, imgtype, image_tag, cmd),
        pty=True, echo=True)


def _get_all_distros(gui=False, include_old=False):
    os.chdir(HERE)
    wildcard = os.path.join('gui' if gui else 'build', '*-*')
    all_matching = sorted(glob.glob(wildcard))
    all_matching = [os.path.basename(item) for item in all_matching]
    if not include_old:
        all_matching = [name for name in all_matching if name not in OLD]
    return all_matching


@task()
def showall(ctx, gui=False, include_old=False):
    """
    Just for easy testing of _get_all_distros()
    """
    images = _get_all_distros(gui, include_old)
    for img in images:
        print(img)
