import os
import glob
import sys
from invoke import task, run


HERE = os.path.abspath(os.path.dirname(__file__))
IMAGE = 'quay.io/pypa/manylinux_2_28_x86_64'
# TODO: Try the aarch64 image.
#       Also, it may be worth trying again to get manylinux_2014 working.

@task(
    help={
        'cmd': "If given will run this command instead of the image's default command.",
        'keep': "Keep the container when it exits. Otherwise it will be auto-removed."
    },
)
def run(ctx, cmd=None, keep=False, extra=''):
    """
    Run the manylinux docker image.
    """
    os.chdir(HERE)
    dist = os.path.abspath('../dist')
    cwd = os.getcwd()
    cmd = '' if cmd is None else cmd
    rm = '' if keep else '--rm'
    ctx.run(
        f'docker run -it {rm} -v {dist}:/dist -v {cwd}:/scripts {extra} {IMAGE} {cmd}',
        pty=True, echo=True)


@task(
    help={
        'pythons': "Comma separated list of Python verions to build for.",
        'keep':    "Keep the container when it exits. Otherwise it will be auto-removed.",
        'interactive': "Run a shell when the build script is done so the container can be examined."
    }
)
def build(ctx, pythons='', keep=False, interactive=False):
    """
    Run the build(s)
    """
    # Ensure we've got a source archive available
    source = glob.glob('../dist/wxPython-*.tar.gz')
    if not source:
        print('ERROR: no source archive found in ../dist')
        sys.exit(1)
    if len(source) > 1:
        print('ERROR: Too many source archives found in ../dist')
        sys.exit(1)
    source = source[0]
    version = source[17:-7]

    pythons = pythons.split(',')
    pythons = ' '.join(pythons)
    cmd = f'/scripts/do-build.sh {version} {pythons}'
    extra = '-e INTERACTIVE=1' if interactive else ''
    run(ctx, cmd, keep, extra)

