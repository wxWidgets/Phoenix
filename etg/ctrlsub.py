#---------------------------------------------------------------------------
# Name:        etg/ctrlsub.py
# Author:      Robin Dunn
#
# Created:     2-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "ctrlsub"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxItemContainerImmutable', 'wxItemContainer', 'wxControlWithItems', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False)  # all classes abstract, no unitests needed
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxItemContainerImmutable')
    c.abstract = True

    c = module.find('wxItemContainer')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    # Ignore the Append and Insert method overloads that we don't want to
    # support. This will keep the ones that take a wxString or an
    # wxArrayString, and wxClientData.
    def pickOverloads(m):
        assert isinstance(m, etgtools.MethodDef)
        if 'void *' in m.argsString or \
           'wxClientData **' in m.argsString or \
           'wxString *' in m.argsString or \
            'std::vector' in m.argsString:
            m.ignore()

    for m in c.findAll('Append'):
        pickOverloads(m)
    for m in c.findAll('Insert'):
        pickOverloads(m)
    for m in c.findAll('Set'):
        pickOverloads(m)


    # The [G|S]etClientData methods deal with untyped void* values, which we
    # don't support. The [G|S]etClientObject methods use wxClientData instances
    # which we have a MappedType for, so make the ClientData methods just be
    # aliases for ClientObjects. From the Python programmer's perspective they
    # would be virtually the same anyway.
    c.find('SetClientObject.data').transfer = True
    c.find('GetClientData').ignore()
    c.find('SetClientData').ignore()
    c.find('GetClientObject').pyName = 'GetClientData'
    c.find('SetClientObject').pyName = 'SetClientData'
    c.addPyMethod('GetClientObject', '(self, n)',
        doc="Alias for :meth:`GetClientData`",
        body="return self.GetClientData(n)")
    c.addPyMethod('SetClientObject', '(self, n, data)',
        doc="Alias for :meth:`SetClientData`",
        body="self.SetClientData(n, data)")


    # Deal with transferring ownership of wxClientData objects
    c.find('DetachClientObject').transfer = True
    c.find('SetClientObject.data').transfer = True
    c.find('Append').findOverload('clientData').find('clientData').transfer = True
    c.find('Insert').findOverload('clientData').find('clientData').transfer = True

    # for compatibility, should they be deprecated?
    c.addPyMethod('AppendItems', '(self, items)',
        doc="Alias for :meth:`Append`",
        body="self.Append(items)")
    c.addPyMethod('GetItems', '(self)',
        doc="Alias for :meth:`GetStrings`",
        body="return self.GetStrings()")
    c.addPyMethod('SetItems', '(self, items)',
        body="self.Set(items)",
        doc="Alias for :meth:`Set`")


    c = module.find('wxControlWithItems')
    c.abstract = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

