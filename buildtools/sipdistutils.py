# Subclasses disutils.command.build_ext,
# replacing it with a SIP version that compiles .sip -> .cpp
# before calling the original build_ext command.
# Written by Giovanni Bajo <rasky at develer dot com>
# Based on Pyrex.Distutils, written by Graham Fawcett and Darrel Gallion.

import distutils.command.build_ext
from distutils.dep_util import newer, newer_group
import os
import sys
from hashlib import sha1

build_ext_base = distutils.command.build_ext.build_ext

def replace_suffix(path, new_suffix):
    return os.path.splitext(path)[0] + new_suffix

class build_ext (build_ext_base):

    description = "Compile SIP descriptions, then build C/C++ extensions (compile/link to build directory)"

    user_options = build_ext_base.user_options[:]
    user_options = [opt for opt in user_options if not opt[0].startswith("swig")]
    user_options += [
        ('sip-opts=', None,
         "list of sip command line options"),
    ]

    def initialize_options (self):
        build_ext_base.initialize_options(self)
        self.sip_opts = None

    def finalize_options (self):
        build_ext_base.finalize_options(self)
        if self.sip_opts is None:
            self.sip_opts = []
        else:
            self.sip_opts = self.sip_opts.split(' ')

    def _get_sip_output_list(self, sbf):
        """
        Parse the sbf file specified to extract the name of the generated source
        files. Make them absolute assuming they reside in the temp directory.
        """
        for L in file(sbf):
            key, value = L.split("=", 1)
            if key.strip() == "sources":
                out = []
                for o in value.split():
                    out.append(os.path.join(self._sip_output_dir(), o))
                return out

        raise RuntimeError("cannot parse SIP-generated '%s'" % sbf)

    def _find_sip(self):
        import sipconfig
        cfg = sipconfig.Configuration()
        if os.name == "nt":
            if not os.path.splitext(os.path.basename(cfg.sip_bin))[1]:
                return cfg.sip_bin + ".exe"
        return cfg.sip_bin

    def _sip_inc_dir(self):
        import sipconfig
        cfg = sipconfig.Configuration()
        return cfg.sip_inc_dir

    def _sip_sipfiles_dir(self):
        import sipconfig
        cfg = sipconfig.Configuration()
        return cfg.default_sip_dir

    def _sip_calc_signature(self):
        sip_bin = self._find_sip()
        return sha1(open(sip_bin, "rb").read()).hexdigest()

    def _sip_signature_file(self):
        return os.path.join(self._sip_output_dir(), "sip.signature")

    def _sip_output_dir(self):
        return self.build_temp
    
    def build_extension (self, ext):
        oldforce = self.force

        if not self.force:
            sip_sources = [source for source in ext.sources if source.endswith('.sip')]
            if sip_sources:
                sigfile = self._sip_signature_file()
                if not os.path.isfile(sigfile):
                    self.force = True
                else:
                    old_sig = open(sigfile).read()
                    new_sig = self._sip_calc_signature()
                    if old_sig != new_sig:
                        self.force = True

        build_ext_base.build_extension(self, ext)

        self.force = oldforce

    def swig_sources (self, sources, extension=None):
        if not self.extensions:
            return

        # Add the SIP include directory to the include path
        if extension is not None:
            extension.include_dirs.append(self._sip_inc_dir())
            depends = extension.depends
        else:
            # pre-2.4 compatibility
            self.include_dirs.append(self._sip_inc_dir())
            depends = []  # ?

        # Filter dependencies list: we are interested only in .sip files,
        # since the main .sip files can only depend on additional .sip
        # files. For instance, if a .h changes, there is no need to
        # run sip again.
        depends = [f for f in depends if os.path.splitext(f)[1] == ".sip"]

        # Create the temporary directory if it does not exist already
        if not os.path.isdir(self._sip_output_dir()):
            os.makedirs(self._sip_output_dir())

        # Collect the names of the source (.sip) files
        sip_sources = []
        sip_sources = [source for source in sources if source.endswith('.sip')]
        other_sources = [source for source in sources if not source.endswith('.sip')]
        generated_sources = []

        sip_bin = self._find_sip()

        for sip in sip_sources:
            # Use the sbf file as dependency check
            sipbasename = os.path.basename(sip)
            sbf = os.path.join(self._sip_output_dir(), replace_suffix(sipbasename, ".sbf"))
            if newer_group([sip]+depends, sbf) or self.force:
                self._sip_compile(sip_bin, sip, sbf)
                open(self._sip_signature_file(), "w").write(self._sip_calc_signature())
            out = self._get_sip_output_list(sbf)
            generated_sources.extend(out)

        return generated_sources + other_sources

    def _sip_compile(self, sip_bin, source, sbf):
        self.spawn([sip_bin] + self.sip_opts +
                    ["-c", self._sip_output_dir(),
                    "-b", sbf,
                    "-I", self._sip_sipfiles_dir(),
                    source])

