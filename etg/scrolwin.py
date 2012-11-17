#---------------------------------------------------------------------------
# Name:        etg/scrolwin.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
import copy

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "scrolwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxScrolled' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    scrolled = module.find('wxScrolled')
    assert isinstance(scrolled, etgtools.ClassDef)

    scrolled.find('GetViewStart').findOverload('()').ignore()
    scrolled.find('GetViewStart.x').out = True
    scrolled.find('GetViewStart.y').out = True
    
    m = scrolled.find('CalcScrolledPosition').findOverload('xx')
    m.find('xx').out = True
    m.find('yy').out = True

    m = scrolled.find('CalcUnscrolledPosition').findOverload('xx')
    m.find('xx').out = True
    m.find('yy').out = True

    scrolled.find('GetScrollPixelsPerUnit.xUnit').out = True
    scrolled.find('GetScrollPixelsPerUnit.yUnit').out = True
    
    scrolled.find('GetVirtualSize.x').out = True
    scrolled.find('GetVirtualSize.y').out = True

        
    if True:
        # Now that SIP has the ability to support template classes where the
        # base class is the template parameter, then we can use this instead
        # of the trickery in the other branch below.
        
        # Doxygen doesn't declare the base class (the template parameter in
        # this case) so we can just add it here.
        # FIXED in Dox 1.8.x
        #scrolled.bases.append('T')
        
        scrolled.addPrivateCopyCtor()
        scrolled.addPrivateAssignOp()
        tools.fixWindowClass(scrolled)

        # Add back some virtuals that were removed in fixWindowClass
        scrolled.find('OnDraw').isVirtual = True
        scrolled.find('GetSizeAvailableForScrollTarget').isVirtual = True
        scrolled.find('GetSizeAvailableForScrollTarget').ignore(False)
        scrolled.find('SendAutoScrollEvents').isVirtual = True
        
        # The wxScrolledWindow and wxScrolledCanvas typedefs will be output
        # normally and SIP will treat them like classes that have a
        # wxScrolled mix-in as one of their base classes. Let's add some more
        # info to them for the doc generators.
        docBase = """\
        The :ref:`{name}` class is a combination of the :ref:`{base}` and
        :ref:`Scrolled` classes, and manages scrolling for its client area,
        transforming the coordinates according to the scrollbar positions,
        and setting the scroll positions, thumb sizes and ranges according to
        the area in view.
        """
        item = module.find('wxScrolledWindow')
        assert isinstance(item, etgtools.TypedefDef)
        item.docAsClass = True
        item.bases = ['wxPanel', 'wxScrolled']
        item.briefDoc = docBase.format(name='ScrolledWindow', base='Panel')        
        
        item = module.find('wxScrolledCanvas')
        item.docAsClass = True
        item.bases = ['wxWindow', 'wxScrolled']
        item.briefDoc = docBase.format(name='ScrolledCanvas', base='Window')
        item.detailedDoc[0] = "This scrolled window is not intended to have children "\
                              "so it doesn't have special handling for TAB traversal "\
                              "or focus management."
        
        
    else:
        # NOTE: We do a tricky tweak here because wxScrolled requires using
        # a template parameter as the base class, which SIP doesn't handle
        # yet. So instead we'll just copy the current extractor elements for
        # wxScrolled and morph it into nodes that will generate wrappers for
        # wxScrolledWindow and wxScrolledCanvas as if they were non-template
        # classes.

        # First ignore the existing typedefs
        module.find('wxScrolledWindow').ignore()
        module.find('wxScrolledCanvas').ignore()

        swDoc = " This class derives from wxPanel so it shares its behavior with regard "\
                "to TAB traversal and focus handling.  If you do not want this then use "\
                "wxScrolledCanvas instead."
        scDoc = " This scrolled window is not intended to have children so it doesn't "\
                "have special handling for TAB traversal or focus management."
        
        # Make the copies and add them to the module
        for name, base, doc in [ ('wxScrolledCanvas', 'wxWindow', scDoc),
                                 ('wxScrolledWindow', 'wxPanel', swDoc), ]:
            node = copy.deepcopy(scrolled)
            assert isinstance(node, etgtools.ClassDef)
            node.name = name
            node.templateParams = []
            node.bases = [base]
            node.briefDoc = etgtools.flattenNode(node.briefDoc, False)
            node.briefDoc = node.briefDoc.replace('wxScrolled', name)
            # TODO: replace wxScrolled in the detailedDoc too?
            node.briefDoc += doc
            for ctor in node.find('wxScrolled').all():
                ctor.name = name

            node.addPrivateCopyCtor()
            node.addPrivateAssignOp()
            tools.fixWindowClass(node)

            # Add back some virtuals that were removed in fixWindowClass
            node.find('OnDraw').isVirtual = True
            node.find('GetSizeAvailableForScrollTarget').isVirtual = True
            node.find('GetSizeAvailableForScrollTarget').ignore(False)
            node.find('SendAutoScrollEvents').isVirtual = True
            
            module.insertItemAfter(scrolled, node)
            
        # Ignore the wxScrolled template class
        scrolled.ignore()
        
    
    module.addPyCode("PyScrolledWindow = wx.deprecated(ScrolledWindow, 'Use ScrolledWindow instead.')")
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

