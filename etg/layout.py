#---------------------------------------------------------------------------
# Name:        etg/layout.py
# Author:      Robin Dunn
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "layout"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxIndividualLayoutConstraint',
           'wxLayoutConstraints'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxIndividualLayoutConstraint')
    assert isinstance(c, etgtools.ClassDef)

    c.find('GetOtherWindow').setCppCode('return (wxWindow*)self->GetOtherWindow();')

    c.addProperty('Done GetDone SetDone')
    c.addProperty('Margin GetMargin SetMargin')
    c.addProperty('MyEdge GetMyEdge')
    c.addProperty('OtherEdge GetOtherEdge')
    c.addProperty('OtherWindow GetOtherWindow')
    c.addProperty('Percent GetPercent')
    c.addProperty('Relationship GetRelationship SetRelationship')
    c.addProperty('Value GetValue SetValue')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

