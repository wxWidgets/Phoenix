import os
import glob
import sys
from invoke import task, run

HERE = os.path.abspath(os.path.dirname(__file__))
IMAGE = 'quay.io/pypa/manylinux_2_28_{}'


@task(
    help={
        'cmd': "If given will run this command instead of the image's default command.",
        'keep': "Keep the container when it exits. Otherwise it will be auto-removed.",
        'extra': "Extra flags to pass to the docker command line.",
        'arch': 'The architecture to build for. "x86_64" (default) or "aarch64".'
    },
)
def run(ctx, cmd=None, keep=False, extra='', arch='x86_64'):
    """
    Run the manylinux docker image.
    """
    os.chdir(HERE)
    dist = os.path.abspath('../dist')
    cwd = os.getcwd()
    cmd = '' if cmd is None else cmd
    rm = '' if keep else '--rm'
    image = IMAGE.format(arch)
    ctx.run(
        f'docker run -it {rm} -v {dist}:/dist -v {cwd}:/scripts {extra} {image} {cmd}',
        pty=True, echo=True)


@task(
    help={
        'pythons': "Comma separated list of Python verions to build for.",
        'keep':    "Keep the container when it exits. Otherwise it will be auto-removed.",
        'interactive': "Run a shell when the build script is done so the container can be examined.",
        'arch': 'The architecture to build for. "x86_64" (default) or "aarch64".'
    }
)
def build(ctx, pythons='', keep=False, interactive=False, arch='x86_64'):
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
    if pythons == 'all':
        pythons = '3.8, 3.9, 3.10'
    if pythons == '':
        pythons = '3.8'

    pythons = pythons.split(',')
    pythons = ' '.join(pythons)
    cmd = f'/scripts/do-build.sh {version} {pythons}'
    extra = '-e INTERACTIVE=yes' if interactive else ''
    run(ctx, cmd, keep, extra, arch)

