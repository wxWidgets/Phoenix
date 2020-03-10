#---------------------------------------------------------------------------
# Name:        etg/sound.py
# Author:      Robin Dunn
#
# Created:     15-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "sound"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSound",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/sound.h>')
    module.addHeaderCode('#include "wxpybuffer.h"')

    c = module.find('wxSound')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.find('Play').mustHaveApp()
    c.find('Stop').mustHaveApp()
    c.addPrivateCopyCtor()
    c.addPublic()

    c.find('wxSound').findOverload('data').ignore()
    #c.addCppCtor_sip('(wxPyBuffer* data)',
    #    useDerivedName=True,
    #    doc="Create a sound object from data in a memory buffer in WAV format.",
    #    body="""\
    #        sipCpp = new sipwxSound();
    #        sipCpp->Create((size_t)data->m_len, data->m_ptr);
    #        """)


    c.find('Create').findOverload('data').ignore()
    c.addCppMethod('bool', 'CreateFromData', '(wxPyBuffer* data)',
        doc="Create a sound object from data in a memory buffer in WAV format.",
        body="return self->Create((size_t)data->m_len, data->m_ptr);")


    c.find('wxSound.isResource').ignore()
    c.find('Create.isResource').ignore()

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.find('Play').renameOverload('filename', 'PlaySound')
    c.find('IsPlaying').ignore()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

