#!/usr/bin/env python
#---------------------------------------------------------------------------
# Name:        bin/make-new-etg-file.py
# Author:      Kevin Ollivier
#
# Created:     24-Sept-2011
# Copyright:   (c) 2015-2020 by Kevin Ollivier, Robin Dunn
# License:     wxWindows License
#---------------------------------------------------------------------------

from datetime import date
from optparse import OptionParser
import os
import sys

script_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(script_dir, ".."))

usage = "usage: %prog [options] name module"
parser = OptionParser(usage)
parser.add_option("-a", "--author", dest="author", default="Robin Dunn")
parser.add_option("-c", "--copyright", dest="copyright", default="Total Control Software")
parser.add_option("-i", "--items", dest="items", default="", help="Comma separated list of classes to wrap")


etgstub = """\
#---------------------------------------------------------------------------
# Name:        etg/%(filename)s
# Author:      %(author)s
#
# Created:     %(date)s
# Copyright:   (c) %(year)s by %(copyright)s
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "%(module)s"
NAME      = "%(name)s"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ %(items)s
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    #module.addHeaderCode('#include <wx/some_header_file.h>')

    #c = module.find('')
    #assert isinstance(c, etgtools.ClassDef)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

"""

# TODO: refactor to just use make-new-unittest-file instead of duplicating it here...

unitteststub = """\
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class %(name)s_Tests(wtc.WidgetTestCase):

    # TODO: Remove this test and add real ones.
    def test_%(name)s1(self):
        self.fail("Unit tests for %(name)s not implemented yet.")

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
"""




def main():
    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        return

    item_str = ""
    for item in options.items.split(","):
        item_str += "'%s',\n" % item

    values = {
        "author"    : options.author,
        "copyright" : options.copyright,
        "items"     : item_str,
        "year"      : date.today().strftime("%Y"),
        "date"      : date.today().strftime("%d-%b-%Y"),
        "name"      : args[0],
        "filename"  : args[0] + ".py",
        "module"    : args[1],
    }

    writeFile(
        os.path.join(root_dir, "etg", values["filename"]), etgstub, values)
    writeFile(
        os.path.join(root_dir, "unittests", "test_%s.py"%values["name"]),
        unitteststub, values)


def writeFile(filename, stub, values):
    if os.path.exists(filename):
        print("'%s' already exists. Exiting." % filename)
        sys.exit(1)
    with open(filename, 'w') as output:
        output.write(stub % values)
    print("Wrote %s" % filename)


if __name__ == '__main__':
    main()
