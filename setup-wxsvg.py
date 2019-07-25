
import sys
import os
import textwrap
from setuptools import setup, Extension
from Cython.Build import cythonize

VERSION = "0.1.0"
DESCRIPTION = ''
LONG_DESCRIPTION = ''
AUTHOR = 'Robin Dunn'
AUTHOR_EMAIL = 'robin@alldunn.com'
URL = ''
DOWNLOAD_URL = ''
LICENSE = ''

HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGE = 'wx.svg'
PACKAGEDIR = 'wx/svg'

with open(os.path.join(HERE, PACKAGEDIR, '_version.py'), 'w') as f:
    f.write(textwrap.dedent(f"""\
        # Generated from {__file__}
        __version__ = '{VERSION}'
        """))

module = Extension(name='wx.svg._nanosvg',
                   sources=['wx/svg/_nanosvg.pyx'],
                   include_dirs=['ext/nanosvg/src'],
                   define_macros=[('NANOSVG_IMPLEMENTATION', '1'),
                                  ('NANOSVGRAST_IMPLEMENTATION', '1'),
                                  ('NANOSVG_ALL_COLOR_KEYWORDS', '1'),
                                  ])

setup(name             = 'nanosvg',
      version          = VERSION,
      description      = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      author           = AUTHOR,
      author_email     = AUTHOR_EMAIL,
      url              = URL,
      download_url     = DOWNLOAD_URL,
      license          = LICENSE,
      packages         = [PACKAGE],
      ext_modules      = cythonize(
                            [module],
                            compiler_directives={'embedsignature': True,
                                                 'language_level':2,
                                                 }),
)
