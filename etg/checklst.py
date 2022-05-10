#---------------------------------------------------------------------------
# Name:        etg/checklst.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     06-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "checklst"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxCheckListBox' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxCheckListBox')
    assert isinstance(c, etgtools.ClassDef)

    c.find('wxCheckListBox').findOverload('wxString choices').ignore()
    c.find('wxCheckListBox').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    c.find('Create').findOverload('wxString choices').ignore()
    c.find('Create').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    c.addCppMethod('wxArrayInt*', 'GetSelections', '()',
        isConst=True, factory=True,
        doc="Returns a list of the indices of the currently selected items.",
        body="""\
            wxArrayInt* array = new wxArrayInt;
            self->GetSelections(*array);
            return array;
            """)

    tools.fixWindowClass(c)


    # We already have the Python methods below, so just ignore this new method for now.
    c.find('GetCheckedItems').ignore()

    c.addPyMethod('GetCheckedItems', '(self)', doc="""\
        GetCheckedItems()

        Return a sequence of integers corresponding to the checked items in
        the control, based on :meth:`IsChecked`.""",
        body="return tuple([i for i in range(self.Count) if self.IsChecked(i)])")

    c.addPyMethod('GetCheckedStrings', '(self)',
        doc="""\
            GetCheckedStrings()

            Return a tuple of strings corresponding to the checked
            items of the control, based on :meth:`GetChecked`.""",
        body="return tuple([self.GetString(i) for i in self.GetCheckedItems()])")

    c.addPyMethod('SetCheckedItems', '(self, indexes)',
        doc="""\
            SetCheckedItems(indexes)

            Sets the checked state of items if the index of the item is
            found in the indexes sequence.""",
        body="""\
            for i in indexes:
                assert 0 <= i < self.Count, "Index (%s) out of range" % i
            for i in range(self.Count):
                self.Check(i, i in indexes)""")

    c.addPyMethod('SetCheckedStrings', '(self, strings)',
        doc="""\
            SetCheckedStrings(strings)

            Sets the checked state of items if the item's string is found
            in the strings sequence.""",
        body="""\
            for s in strings:
                assert s in self.GetStrings(), "String ('%s') not found" % s
            for i in range(self.Count):
                self.Check(i, self.GetString(i) in strings)""")


    c.addPyMethod('GetChecked', '(self)', 'return self.GetCheckedItems()',
                  deprecated='Use GetCheckedItems instead.')
    c.addPyMethod('SetChecked', '(self, indexes)', 'return self.SetCheckedItems(indexes)',
                  deprecated='Use SetCheckedItems instead.')

    c.addPyProperty('Checked GetChecked SetChecked')
    c.addPyProperty('CheckedItems GetCheckedItems SetCheckedItems')
    c.addPyProperty('CheckedStrings GetCheckedStrings SetCheckedStrings')


    tools.fixItemContainerClass(c)
    c.addItem(etgtools.WigCode("""\
        virtual int GetSelections(wxArrayInt& aSelections) const;
        """))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

