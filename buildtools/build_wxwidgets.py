#!/usr/bin/env python

###################################
# Author: Kevin Ollivier
# Licence: wxWindows licence
###################################

import os
import re
import sys
import optparse
import platform
import types
import subprocess

from buildtools import builder

# builder object
wxBuilder = None

# other globals
scriptDir = None
wxRootDir = None
contribDir = None
options = None
configure_opts = None
exitWithException = True

verbose = False


def numCPUs():
    """
    Detects the number of CPUs on a system.
    This approach is from detectCPUs here: http://www.artima.com/weblogs/viewpost.jsp?thread=230001
    """
    # Linux, Unix and MacOS:
    if hasattr(os, "sysconf"):
        if "SC_NPROCESSORS_ONLN" in os.sysconf_names:
            # Linux & Unix:
            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
            if isinstance(ncpus, int) and ncpus > 0:
                return ncpus
        else: # OSX:
            p = subprocess.Popen("sysctl -n hw.ncpu", shell=True, stdout=subprocess.PIPE)
            return p.stdout.read()

    # Windows:
    if "NUMBER_OF_PROCESSORS" in os.environ:
            ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
            if ncpus > 0:
                return ncpus
    return 1 # Default


def getXcodePaths():
    base = getoutput("xcode-select -print-path")
    return [base, base+"/Platforms/MacOSX.platform/Developer"]



def exitIfError(code, msg):
    if code != 0:
        print(msg)
        if exitWithException:
            raise builder.BuildError(msg)
        else:
            sys.exit(1)


def getWxRelease(wxRoot=None):
    if not wxRoot:
        global wxRootDir
        wxRoot = wxRootDir
    with open(os.path.join(wxRoot, "configure.ac"), "r") as fid:
        configureText = fid.read()
    majorVersion = re.search(r"wx_major_version_number=(\d+)", configureText).group(1)
    minorVersion = re.search(r"wx_minor_version_number=(\d+)", configureText).group(1)

    versionText = "%s.%s" % (majorVersion, minorVersion)

    if int(minorVersion) % 2:
        releaseVersion = re.search(r"wx_release_number=(\d+)", configureText).group(1)
        versionText += ".%s" % (releaseVersion)

    return versionText


def run(cmd):
    global verbose
    if verbose:
        print("Running %s" % cmd)
    return exitIfError(os.system(cmd), "Error running %s" % cmd)


def getoutput(cmd):
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = None
    output = sp.stdout.read()
    outputEncoding = 'cp1252' if sys.platform == 'win32' else 'utf-8'
    output = output.decode(outputEncoding)
    output = output.rstrip()
    rval = sp.wait()
    if rval:
        # Failed!
        print("Command '%s' failed with exit code %d." % (cmd, rval))
        sys.exit(rval)
    return output


def main(wxDir, args):
    global wxRootDir
    global contribDir
    global options
    global configure_opts
    global wxBuilder

    wxRootDir = wxDir

    contribDir = os.path.join("contrib", "src")
    installDir = None

    VERSION = tuple([int(i) for i in getWxRelease().split('.')[:2]])

    # wxWidgets is built with CMake on Windows, see wxcmake.py
    toolkit = "autoconf"

    defJobs = str(numCPUs())
    option_dict = {
        "clean"         : (False, "Clean all files from the build directory"),
        "debug"         : (False, "Build the library in debug symbols"),
        "builddir"      : ("", "Directory where the build will be performed for autoconf builds."),
        "prefix"        : ("", "Configured prefix to use for autoconf builds. Defaults to installdir if set."),
        "jobs"          : (defJobs, "Number of jobs to run at one time in make. Default: %s" % defJobs),
        "install"       : (False, "Install the toolkit to the installdir directory, or the default dir."),
        "installdir"    : ("", "Directory where built wxWidgets will be installed"),
        "gtk2"          : (False, "On Linux build for gtk2 (default gtk3"),
        "gtk3"          : (True,  "On Linux build for gtk3"),
        "mac_universal_binary"
                        : ("", "Comma separated list of architectures to include in the Mac universal binary"),
        "no_config"     : (False, "Turn off configure step on autoconf builds"),
        "config_only"   : (False, "Only run the configure step and then exit"),
        "rebake"        : (False, "Regenerate Bakefile and autoconf files"),
        "wxpython"      : (False, "Build the wxWidgets library with all options needed by wxPython"),
        "osx_cocoa"     : (False, "Build the Cocoa port"),
        "shared"        : (False, "Build wx as a dynamic library"),
        "extra_make"    : ("", "Extra args to pass on make's command line."),
        "features"      : ("", "A list of configure flags."),
        "verbose"       : (False, "Print commands as they are run, (to aid with debugging this script)"),
        "set_rpath_origin"
                        : (False, "Set RPATH to $ORIGIN when building wxWidgets libraries"),
    }

    parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")

    for opt in sorted(option_dict):
        default = option_dict[opt][0]
        action = "store"
        if type(default) == bool:
            action = "store_true"
        parser.add_option("--" + opt, default=default, action=action, dest=opt,
                          help=option_dict[opt][1])

    options, arguments = parser.parse_args(args=args)

    global verbose
    if options.verbose:
        verbose = True

    # compiler / build system specific args
    buildDir = options.builddir
    args = []
    installDir = options.installdir
    prefixDir = options.prefix

    if toolkit == "autoconf":
        if not buildDir:
            buildDir = os.getcwd()
        configure_opts = []
        if options.features != "":
            configure_opts.extend(options.features.split(" "))

        if options.debug:
            configure_opts.append("--enable-debug")

        if options.osx_cocoa:
            configure_opts.append("--with-osx_cocoa")

        if options.gtk2:
            options.gtk3 = False

        if not sys.platform.startswith("darwin"):
            if options.gtk3:
                configure_opts.append("--with-gtk=3")

            if options.gtk2:
                configure_opts.append("--with-gtk=2")

        wxpy_configure_opts = [
                            "--enable-sound",
                            "--enable-graphics_ctx",
                            "--enable-display",
                            "--enable-debug_flag",
                            "--enable-optimise",
                            "--disable-debugreport",
                            "--enable-uiactionsim",
                            "--enable-autoidman",
                            ]

        if not sys.platform.startswith("darwin"):
            wxpy_configure_opts.append("--with-sdl")

        if sys.platform.startswith("darwin"):
            universalCapable = False

            # Set the minimum supported OSX version.
            # TODO: Add a CLI option to set this.
            wxpy_configure_opts.append("--with-macosx-version-min=10.10")

            # find the newest SDK available on this system
            SDK = 'none found'
            for xcodePath in getXcodePaths():
                possibles = [(major, minor) for major in [10, 11, 12, 13, 14, 15, 26, 27] for minor in range(16)]
                for major, minor in reversed(possibles):
                    sdk = os.path.join(xcodePath, "SDKs/MacOSX{}.{}.sdk".format(major, minor))
                    if os.path.exists(sdk):
                        # Although we've found a SDK, we're not actually using
                        # it at the moment. The builds seem to work better if we
                        # let the compiler use whatever it considers to be the
                        # default.
                        # wxpy_configure_opts.append("--with-macosx-sdk=%s" % sdk)
                        universalCapable = major >= 11
                        SDK = sdk
                        break

            # Now cross check that if a universal build was requested that it's
            # possible to do with the selected SDK.
            arch = ''
            if options.mac_universal_binary:
                if options.mac_universal_binary == 'default':
                    if universalCapable:
                        arch = "arm64,x86_64"
                    else:
                        arch = "x86_64"
                else:
                    # otherwise assume the user knows what they are doing and just use what they gave us.
                    arch = options.mac_universal_binary
                configure_opts.append("--enable-universal_binary=%s" % arch)

            # print("SDK Path:          {}".format(SDK))
            print("Universal Capable: {}".format(universalCapable))
            print("Architectures:     {}".format(arch))

            wxpy_configure_opts.append("--with-libjpeg=builtin")
            wxpy_configure_opts.append("--with-libpng=builtin")
            wxpy_configure_opts.append("--with-libtiff=builtin")
            wxpy_configure_opts.append("--with-libwebp=builtin")
            wxpy_configure_opts.append("--with-regex=builtin")


        if installDir and not prefixDir:
            prefixDir = installDir
        if prefixDir:
            prefixDir = os.path.abspath(prefixDir)
            configure_opts.append("--prefix=" + prefixDir)


        if options.wxpython:
            configure_opts.extend(wxpy_configure_opts)
            if options.debug:
                # wxPython likes adding these debug options too
                configure_opts.append("--enable-debug_gdb")
                configure_opts.append("--disable-optimise")
                configure_opts.remove("--enable-optimise")


        if options.rebake:
            retval = run("make -f autogen.mk")
            exitIfError(retval, "Error running autogen.mk")

        # Workaround OpenSUSE libdir issue by unsetting CONFIG_SITE envvar
        env = None
        if "CONFIG_SITE" in os.environ:
            env = dict(os.environ)
            del env["CONFIG_SITE"]

        if options.set_rpath_origin:
            configure_opts.append("--disable-rpath")
            configure_opts.append(r"LDFLAGS='-Wl,-rpath,\$$ORIGIN'")

        print("Configure options: " + repr(configure_opts))
        wxBuilder = builder.AutoconfBuilder()
        if not options.no_config and not options.clean:
            olddir = os.getcwd()
            if buildDir:
                os.chdir(buildDir)
            exitIfError(wxBuilder.configure(dir=wxRootDir, options=configure_opts, env=env),
                        "Error running configure")
            os.chdir(olddir)

        if options.config_only:
            print("Exiting after configure")
            return


    if not wxBuilder:
        print("Builder not available for your specified platform/compiler.")
        sys.exit(1)

    if options.clean:
        print("Performing cleanup.")
        wxBuilder.clean(dir=buildDir, options=args)

        sys.exit(0)

    if options.extra_make:
        args.append(options.extra_make)

    args.append("--jobs=" + options.jobs)
    exitIfError(wxBuilder.build(dir=buildDir, options=args), "Error building")

    if options.install:
        extra=None
        if installDir:
            extra = ['DESTDIR='+installDir]
        wxBuilder.install(dir=buildDir, options=extra)

if __name__ == '__main__':
    exitWithException = False  # use sys.exit instead
    main(sys.argv[0], sys.argv[1:])
