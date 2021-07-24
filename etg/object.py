#---------------------------------------------------------------------------
# Name:        etg/object.py
# Author:      Robin Dunn
#
# Created:     9-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "object"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
    'wxRefCounter',
    'wxObject',
    'wxClassInfo',
    #'wxObjectDataPtr',
    'classwx_object_data_ptr_3_01_t_01_4.xml',
    ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    module.find('wxCreateDynamicObject').ignore()


    #--------------------------------------------------
    c = module.find('wxClassInfo')
    assert isinstance(c, etgtools.ClassDef)
    module.insertItemBefore(c, etgtools.TypedefDef(type='void*', name='wxObjectConstructorFn'))
    module.find('wxClassInfo').abstract = True
    module.find('wxClassInfo.wxClassInfo').ignore()


    #--------------------------------------------------
    c = module.find('wxRefCounter')
    assert isinstance(c, etgtools.ClassDef)
    c.find('~wxRefCounter').ignore(False)
    c.addPrivateCopyCtor()
    tools.fixRefCountedClass(c)


    #--------------------------------------------------
    c = module.find('wxObject')
    c.find('operator delete').ignore()
    c.find('operator new').ignore()
    c.find('IsKindOf').ignore()

    # EXPERIMENTAL: By turning off the virtualness of the wxObject dtor, and
    # since there are no other virtuals that we are exposing here, then all
    # classes that derive from wxObject that do not have any virtuals of
    # their own (or have the virtual flags turned off by the tweaker code)
    # can have simpler wrappers generated for them with no extra derived
    # class whose only purpose is to reflect calls to the virtual methods to
    # Python implementations. (And since the only virtual is the dtor then
    # that is of no real benefit to Python code since we're not overriding
    # the dtor anyhow.) In addition it appears so far that none of these
    # classes would ever need to have Python derived classes anyway. This
    # also makes it easier and less SIP-specific to add or replace ctors in
    # those classes with custom C++ code. (See wxFont and wxAcceleratorTable
    # for examples.)
    c.find('~wxObject').isVirtual = False
    c.find('GetClassInfo').isVirtual = False

    c.addCppMethod('const wxChar*', 'GetClassName', '()',
        body='return self->GetClassInfo()->GetClassName();',
        doc='Returns the class name of the C++ class using wxRTTI.')

    c.addCppMethod('void', 'Destroy', '()',
        body='delete self;',
        doc='Deletes the C++ object this Python object is a proxy for.',
        transferThis=True)  # TODO: Check this


    tools.addSipConvertToSubClassCode(c)

    #-----------------------------------------------------------------
    c = module.find('wxObjectDataPtr< T >')
    c.name = 'wxObjectDataPtr'
    c.piIgnored = True
    c.docsIgnored = True

    # fix up the ctor/dtor due to name change above
    ctor = c.find('wxObjectDataPtr')
    ctor.isCtor = True
    dtor = c.find('~wxObjectDataPtr')
    dtor.isDtor = True

    ctor.findOverload('< U >').ignore()

    # more name hacks/fixes
    c.nodeBases = ({'wxObjectDataPtr': ('wxObjectDataPtr', [])},
                   ['wxObjectDataPtr'])

    # ignore the smart pointer methods, for now
    c.find('operator->').ignore()
    c.find('operator*').ignore()
    c.find('operator unspecified_bool_type').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

