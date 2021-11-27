#----------------------------------------------------------------------
# Name:        buildtools.wxpysip
# Purpose:     Code to help migrate to SIP 5 with as little disruption
#              as possible.
#
# Author:      Robin Dunn
#
# Created:     4-Jan-2021
# Copyright:   (c) 2021 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

# NOTE: This code is mostly copied, adapted, and extended from the
#       sipbuild.legacy.sip5 module. The main intent is to make it easy to run
#       sip the same way as the legacy sip5 entry point, but without needing to
#       run a subprocess, and to also add a little missing sip 4 functionality
#       that we were depending on with the old SIP.
import os

from sipbuild.code_generator import (set_globals, parse, generateCode,
        generateExtracts, generateAPI, generateXML, generateTypeHints)
from sipbuild.exceptions import handle_exception, UserException
from sipbuild.module import resolve_abi_version
from sipbuild.version import SIP_VERSION, SIP_VERSION_STR


def sip_runner(
    specification,              # the name of the specification file [default stdin]
    sources_dir=None,           # the name of the code output directory [default not generated]
    include_dirs=[],            # add <DIR> to the list of directories to search when importing or including .sip files
    warnings=False,             # enable warning messages [default disabled]
    docstrings=False,           # enable the automatic generation of docstrings [default disabled]
    release_gil=False,          # always release and reacquire the GIL [default only when specified]
    sip_module=None,            # the fully qualified name of the sip module
    api_extract=None,           # the name of the QScintilla API file [default not generated
    exceptions=False,           # enable support for C++ exceptions [default disabled]
    tracing=False,              # generate code with tracing enabled [default disabled]
    extracts=[],                # add <ID:FILE> to the list of extracts to generate
    pyi_extract=None,           # the name of the .pyi stub file [default not generated]
    sbf_file=None,              # File to write the generated file lists to [default not generated]
    abi_version=None,           # the sip ABI version
    backstops=[],               # add <TAG> to the list of timeline backstops
    py_debug=False,             # generate code for a debug build of Python
    warnings_are_errors=False,  # warnings are handled as errors
    parts=0,                    # split the generated code into <FILES> files [default 1 per class]
    xml_extract=None,           # file to write sip xml to
    protected_is_public=False,  # enable the protected/public hack [default disabled]
    source_suffix=None,         # the suffix to use for C or C++ source files [default \".c\" or \".cpp\"]
    tags=[],                    # add <TAG> to the list of versions/platforms to generate code for
    disabled_features=[],       # add <FEATURE> to the list of disabled features
    ):

    print("Running SIP code generator on: {}".format(specification))

    generated_files = []
    try:
        # The code generator requires the name of the sip module.
        if sources_dir is not None and sip_module is None:
            raise UserException("the name of the sip module must be given")

        # Check the ABI version.
        abi_major, abi_minor = resolve_abi_version(abi_version).split('.')

        # Set the globals.
        sip_major_version = SIP_VERSION >> 16
        if sip_major_version >= 6:
            set_globals(SIP_VERSION, SIP_VERSION_STR, int(abi_major), int(abi_minor),
                        sip_module, UserException, include_dirs)
        else:
            set_globals(SIP_VERSION, SIP_VERSION_STR, int(abi_major), int(abi_minor),
                        UserException, include_dirs)

        # Parse the input file.
        pt, _, _, _, tags, disabled_features = parse(specification,
                (xml_extract is None), tags, backstops, disabled_features,
                protected_is_public)

        # Generate the bindings.
        if sources_dir is not None:
            generate_args = [pt, sources_dir, source_suffix,
                             exceptions, tracing, release_gil, parts, tags,
                             disabled_features, docstrings, py_debug]
            if sip_major_version < 6:
                generate_args.append(sip_module)
            generated_files = generateCode(*generate_args)

        if sbf_file is not None:
            generateBuildFile(sbf_file, generated_files)

        # Generate any extracts.
        generateExtracts(pt, extracts)

        # Generate the API file.
        if api_extract is not None:
            generateAPI(pt, api_extract)

        # Generate the type hints file.
        if pyi_extract is not None:
            generateTypeHints(pt, pyi_extract)

        # Generate the XML file.
        if xml_extract is not None:
            generateXML(pt, xml_extract)

    except Exception as e:
        handle_exception(e)

    return generated_files


def generateBuildFile(sbf_file, generated_files):
    header, sources = generated_files
    header = os.path.basename(header)
    sources = [os.path.basename(n) for n in sources]
    with open(sbf_file, 'w') as f:
        f.write("sources = {}\n".format(' '.join(sources)))
        f.write("headers = {}\n".format(header))
