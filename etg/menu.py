#---------------------------------------------------------------------------
# Name:        etg/menu.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "menu"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxMenu', 'wxMenuBar' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    def addTransferAnnotations(c, arg):
        for method in c.findAll('Append') + c.findAll('Insert') + \
                      c.findAll('Replace') + c.findAll('Prepend'):
            arg_def = method.findItem(arg)
            if arg_def:
                arg_def.transfer = True

        for method in c.findAll('Remove') + c.findAll('Replace'):
            method.transferBack = True


    #-----------------------------------------------------------------
    c = module.find('wxMenu')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    tools.removeVirtuals(c)
    c.find('Prepend.item').name = 'menuItem'
    c.find('Prepend.submenu').name = 'subMenu'

    addTransferAnnotations(c, 'menuItem')
    addTransferAnnotations(c, 'subMenu')
    c.find('AppendSubMenu.submenu').transfer = True
    c.find('Insert.submenu').transfer = True

    # We only need one of these overloads, the non-const/const is not enough
    # to distinguish a unique Python signature.
    c.find('GetMenuItems').overloads = []

    # Ensure that no copy is made of the list object, so we only wrap the
    # existing object and keep it owned by C++
    c.find('GetMenuItems').noCopy = True


    c.addPyMethod('AppendMenu', '(self, id, item, subMenu, help="")', deprecated='Use Append instead.',
                  body='return self.Append(id, item, subMenu, help)')
    c.addPyMethod('AppendItem', '(self, menuItem)', deprecated='Use Append instead.',
                  body='return self.Append(menuItem)')

    c.addPyMethod('InsertMenu', '(self, pos, id, item, subMenu, help="")', deprecated='Use Insert instead.',
                  body='return self.Insert(pos, id, item, subMenu, help)')
    c.addPyMethod('InsertItem', '(self, pos, menuItem)', deprecated='Use Insert instead.',
                  body='return self.Insert(pos, menuItem)')

    c.addPyMethod('PrependMenu', '(self, id, item, subMenu, help="")', deprecated='Use Prepend instead.',
                  body='return self.Prepend(id, item, subMenu, help)')
    c.addPyMethod('PrependItem', '(self, menuItem)', deprecated='Use Prepend instead.',
                  body='return self.Prepend(menuItem)')

    c.addPyMethod('RemoveMenu', '(self, id, item, subMenu, help="")', deprecated='Use Remove instead.',
                  body='return self.Remove(id, item, subMenu, help)')
    c.addPyMethod('RemoveItem', '(self, menuItem)', deprecated='Use Remove instead.',
                  body='return self.Remove(menuItem)')

    # Don't hide the Destroy inherited from wxObject
    c.find('Destroy').findOverload('int').pyName = 'DestroyItem'
    c.find('Destroy').findOverload('wxMenuItem').pyName = 'DestroyItem'

    c.find('FindChildItem.pos').out = True
    c.find('FindItem.menu').out = True
    c.addCppMethod('wxMenuItem*', 'FindItemById', '(int id)', isConst=True,
        doc="""\
            FindItemById(id) -> MenuItem

            Finds the menu item object associated with the given menu item identifier.""",
        body="""\
            return self->FindItem(id);""")

    c.find('MSWCommand').ignore()

    #-----------------------------------------------------------------
    c = module.find('wxMenuBar')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    tools.removeVirtuals(c)
    addTransferAnnotations(c, 'menu')
    c.find('wxMenuBar').findOverload('wxMenu *menus[], const wxString titles[], long style=0)').ignore()

    c.find('FindItem.menu').out = True
    c.addCppMethod('wxMenuItem*', 'FindItemById', '(int id)', isConst=True,
        doc="""\
            FindItemById(id) -> MenuItem

            Finds the menu item object associated with the given menu item identifier.""",
        body="""\
            return self->FindItem(id);""")


    mac_scmb = c.find('MacSetCommonMenuBar')
    mac_scmb.setCppCode("""\
    #ifdef __WXMAC__
        wxMenuBar::MacSetCommonMenuBar(menubar);
    #endif
    """)

    mac_gcmb = c.find('MacGetCommonMenuBar')
    mac_gcmb.setCppCode("""\
    #ifdef __WXMAC__
        return wxMenuBar::MacGetCommonMenuBar();
    #else
        return NULL;
    #endif
    """)

    mac_gcmb = c.find('OSXGetAppleMenu')
    mac_gcmb.setCppCode("""\
    #ifdef __WXMAC__
        return self->OSXGetAppleMenu();
    #else
        return NULL;
    #endif
    """)

    # don't transfer on other platforms, as this is a no-op there.
    import sys
    if sys.platform.startswith('darwin'):
        mac_scmb.find('menubar').transfer = True

    c.find('FindItem.menu').out = True


    c.addPyMethod('GetMenus', '(self)',
        doc="""\
        GetMenus() -> (menu, label)\n
        Return a list of (menu, label) items for the menus in the :class:`MenuBar`.""",
        body="""\
        return [(self.GetMenu(i), self.GetMenuLabel(i)) for i in range(self.GetMenuCount())]
        """)
    c.addPyMethod('SetMenus', '(self, items)',
        doc="""\
        SetMenus()\n
        Clear and add new menus to the :class:`MenuBar` from a list of (menu, label) items.""",
        body="""\
        for i in range(self.GetMenuCount()-1, -1, -1):
            self.Remove(i)
        for m, l in items:
            self.Append(m, l)
        """)
    c.addPyProperty('Menus GetMenus SetMenus')


    # deprecated and removed
    c.find('GetLabelTop').ignore()
    c.find('SetLabelTop').ignore()

    module.addItem(tools.wxListWrapperTemplate('wxMenuList', 'wxMenu', module))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

