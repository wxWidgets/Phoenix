#!/usr/bin/env python

#---------------------------------------------------------------------------
# Name:        etgtools/make-new-etg-file.py
# Author:      Kevin Ollivier
#
# Created:     24-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
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


etgstub = """#---------------------------------------------------------------------------
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
ITEMS  = [ 
    %(items)s
]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

"""

(options, args) = parser.parse_args()

item_str = ""
for item in options.items.split(","):
    item_str += '"%s",\n' % item

arg_dict = {
    "author"    : options.author,
    "copyright" : options.copyright,
    "items"     : item_str,
    "year"      : date.today().strftime("%Y"),
    "date"      : date.today().strftime("%d-%b-%Y"),
    "name"      : args[0],
    "filename"  : args[0] + ".py",
    "module"    : args[1],
}

output_file = os.path.join(root_dir, "etg", arg_dict["filename"])

if os.path.exists(output_file):
    print "Bindings with this name already exist. Exiting."
    sys.exit(1)

output = open(output_file, 'w')
output.write(etgstub % arg_dict)
output.close()

