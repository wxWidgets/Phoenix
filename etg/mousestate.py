#---------------------------------------------------------------------------
# Name:        etg/mousestate.py
# Author:      Robin Dunn
#
# Created:     15-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "mousestate"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxMouseState' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxMouseState')
    c.find('GetPosition').findOverload('int *x').ignore()

    c.addProperty("x GetX SetX")
    c.addProperty("y GetY SetY")
    c.addProperty("X GetX SetX")
    c.addProperty("Y GetY SetY")
    c.addProperty("leftIsDown LeftIsDown SetLeftDown")
    c.addProperty("middleIsDown MiddleIsDown SetMiddleDown")
    c.addProperty("rightIsDown RightIsDown SetRightDown")
    c.addProperty("aux1IsDown Aux1IsDown SetAux1Down")
    c.addProperty("aux2IsDown Aux2IsDown SetAux2Down")
    c.addProperty("Position GetPosition SetPosition")


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

