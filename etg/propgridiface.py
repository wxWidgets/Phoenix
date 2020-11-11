#---------------------------------------------------------------------------
# Name:        etg/propgridiface.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgridiface"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPGPropArgCls',
           'wxPropertyGridInterface',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # These are duplicates, ignore the ones in this module
    module.find('wxPG_PROPERTYVALUES_FLAGS').ignore()
    module.find('wxPG_LABEL').ignore()
    module.find('wxPG_LABEL_STRING').ignore()
    module.find('wxPG_COLOUR_BLACK').ignore()
    module.find('wxPG_COLOUR').ignore()
    module.find('wxPG_DEFAULT_IMAGE_SIZE').ignore()


    #----------------------------------------------------------
    c = module.find('wxPGPropArgCls')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxPGPropArgCls').findOverload('wxString &').ignore()
    c.find('wxPGPropArgCls').findOverload('char *').ignore()
    c.find('wxPGPropArgCls').findOverload('wchar_t *').ignore()
    c.find('wxPGPropArgCls').findOverload('int').ignore()
    c.find('wxPGPropArgCls').findOverload('deallocPtr').ignore()

    # Make a string ctor that uses the wxPython-specific version of
    # the C++ class' ctor
    newCtor = c.addCppCtor('(const wxString& str)',
        doc="Creates a PGPropArgCls from a string.",
        body="""\
            wxString* name = new wxString(*str);
            return new wxPGPropArgCls(name, true);
        """
        )

    # Make it be the first overload instead of the last
    ctor = c.find('wxPGPropArgCls')
    overloads = list(ctor.overloads)
    del overloads[overloads.index(newCtor)]
    overloads.insert(0, newCtor)
    ctor.overloads = overloads


    c.find('GetPtr').overloads[0].ignore()

    c.convertFromPyObject = """\
        // Code to test a PyObject for compatibility with wxPGPropArgCls
        if (!sipIsErr) {
            if (sipCanConvertToType(sipPy, sipType_wxPGPropArgCls, SIP_NO_CONVERTORS))
                return TRUE;
            if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy))
                return TRUE;
            if (sipPy == Py_None)
                return TRUE;
            if (sipCanConvertToType(sipPy, sipType_wxPGProperty, SIP_NO_CONVERTORS))
                return TRUE;
            return FALSE;
        }

        // Code to convert a compatible PyObject to a wxPGPropArgCls
        if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy)) {
            wxString* name = new wxString(Py2wxString(sipPy));
            *sipCppPtr = new wxPGPropArgCls(name, true);
            return sipGetState(sipTransferObj);
        }
        else if (sipCanConvertToType(sipPy, sipType_wxPGProperty, SIP_NO_CONVERTORS)) {
            int state = 0;
            wxPGProperty* prop = reinterpret_cast<wxPGProperty*>(
                sipConvertToType(sipPy, sipType_wxPGProperty, sipTransferObj, SIP_NO_CONVERTORS, &state, sipIsErr));
            *sipCppPtr = new wxPGPropArgCls(prop);
            sipReleaseType(prop, sipType_wxPGProperty, state);
            return sipGetState(sipTransferObj);
        }
        else if (sipPy == Py_None) {
            *sipCppPtr = new wxPGPropArgCls(static_cast< wxPGProperty * >(NULL));
            return sipGetState(sipTransferObj);
        }
        else {
            // It's already a wxPGPropArgCls, just fetch the pointer and return
            *sipCppPtr = reinterpret_cast<wxPGPropArgCls*>(sipConvertToType(
                sipPy, sipType_wxPGPropArgCls, sipTransferObj,
                SIP_NO_CONVERTORS, 0, sipIsErr));
            return 0; // not a new instance
        }
        """


    #----------------------------------------------------------
    c = module.find('wxPropertyGridInterface')
    c.abstract = True
    for m in c.findAll('GetIterator'):
        if m.type == 'wxPropertyGridConstIterator':
            m.ignore()

    tools.ignoreConstOverloads(c)

    spv = c.find('SetPropertyValue')
    spv.findOverload('int value').ignore()
    spv.findOverload('wxLongLong value').ignore()
    spv.findOverload('wxLongLong_t value').ignore()
    spv.findOverload('wxULongLong value').ignore()
    spv.findOverload('wxULongLong_t value').ignore()
    spv.findOverload('wxObject *value').ignore()
    spv.findOverload('wchar_t *value').ignore()
    spv.findOverload('char *value').ignore()

    # Reorder SetPropertyValue overloads so the one taking a long int is not
    # first. Mark others that could be auto-converted from int as
    # "constrained" so they will only be used for that specific type. This
    # should result in SetPropertyValue(id, double) only used for floats and
    # not ints, or other things that can convert to int.
    spv.findOverload('bool value').find('value').constrained = True
    spv.findOverload('double value').find('value').constrained = True
    spv_long = spv.findOverload('long value')
    spv_long.ignore()
    spv.reorderOverloads() # Ensures an ignored item is not first,
    spv_long.ignore(False) # and then we can unignore it.


    c.find('Append.property').transfer = True
    c.find('AppendIn.newProperty').transfer = True
    for m in c.find('Insert').all():
        m.find('newProperty').transfer = True

    # Fix some syntax that sip doesn't like
    p = c.find('GetPropertiesWithFlag.iterFlags')
    if p.default.startswith('('):
        p.default = p.default[1:-1]


    # Tons of Python method implementations ported from Classic...

    module.addPyCode("""\
        _type2property = None
        _vt2getter = None
        """)

    c.addPyMethod('MapType', '(self, class_, factory)',
        doc="""\
            Registers Python type/class to property mapping.

            :param `factory`: Property builder function/class.
            """,
        body="""\
            global _type2property
            if _type2property is None:
                raise AssertionError("call only after a propertygrid or "
                                     "manager instance constructed")
            _type2property[class_] = factory
            """)


    c.addPyMethod('DoDefaultTypeMappings', '(self)',
        doc="Add built-in properties to the map.",
        body="""\
            import sys
            global _type2property
            if _type2property is not None:
                return
            _type2property = dict()

            _type2property[str] = StringProperty
            if sys.version_info.major < 2:
                _type2property[unicode] = StringProperty
            _type2property[int] = IntProperty
            _type2property[float] = FloatProperty
            _type2property[bool] = BoolProperty
            _type2property[list] = ArrayStringProperty
            _type2property[tuple] = ArrayStringProperty
            _type2property[wx.Font] = FontProperty
            _type2property[wx.Colour] = ColourProperty
            #_type2property[wx.Size] = SizeProperty
            #_type2property[wx.Point] = PointProperty
            #_type2property[wx.FontData] = FontDataProperty
            """)


    # TODO: is this still needed?
    c.addPyMethod('DoDefaultValueTypeMappings', '(self)',
        doc="Map pg value type ids to getter methods.",
        body="""\
            global _vt2getter
            if _vt2getter is not None:
                return
            _vt2getter = dict()
        """)


    c.find('GetPropertyValues').ignore()
    c.addPyMethod('GetPropertyValues',
        '(self, dict_=None, as_strings=False, inc_attributes=False, flags=PG_ITERATE_PROPERTIES)',
        doc="""\
            Returns all property values in the grid.

            :param `dict_`: A diftionary to fill with the property values.
                If not given, then a new one is created. The dict_ can be an
                object as well, in which case it's __dict__ is used.
            :param `as_strings`: if True, then string representations of values
                are fetched instead of native types. Useful for config and such.
            :param `inc_attributes`: if True, then property attributes are added
                in the form of ``"@<propname>@<attr>"``.
            :param `flags`: Flags to pass to the iterator. See :ref:`wx.propgrid.PG_ITERATOR_FLAGS`.
            :returns: A dictionary with values. It is always a dictionary,
                so if dict_ was an object with __dict__ attribute, then that
                attribute is returned.
            """,
        body="""\
            if dict_ is None:
                dict_ = {}
            elif hasattr(dict_,'__dict__'):
                dict_ = dict_.__dict__

            getter = self.GetPropertyValue if not as_strings else self.GetPropertyValueAsString

            it = self.GetVIterator(flags)
            while not it.AtEnd():
                p = it.GetProperty()
                name = p.GetName()
                dict_[name] = getter(p)

                if inc_attributes:
                    attrs = p.GetAttributes()
                    if attrs and len(attrs):
                        dict_['@%s@attr'%name] = attrs

                it.Next()

            return dict_
            """)


    for m in c.find('SetPropertyValues').all():
        m.ignore()
    c.addPyMethod('SetPropertyValues', '(self, dict_, autofill=False)',
        doc="""\
            Sets property values from a dictionary.\n
            :param `dict_`: the source of the property values to set, which can be
                either a dictionary or an object with a __dict__ attribute.
            :param `autofill`: If true, keys with not relevant properties are
                auto-created. For more info, see :method:`AutoFill`.

            :note:
              * Keys starting with underscore are ignored.
              * Attributes can be set with entries named like "@<propname>@<attr>".
            """,
        body="""\
            if dict_ is None:
                dict_ = {}
            elif hasattr(dict_,'__dict__'):
                dict_ = dict_.__dict__
            attr_dicts = []

            def set_sub_obj(k0, dict_):
                for k,v in dict_.items():
                    if k[0] != '_':
                        if k.endswith('@attr'):
                            attr_dicts.append((k[1:-5],v))
                        else:
                            try:
                                self.SetPropertyValue(k,v)
                            except:
                                try:
                                    if autofill:
                                        self._AutoFillOne(k0,k,v)
                                        continue
                                except:
                                    if isinstance(v,dict):
                                        set_sub_obj(k,v)
                                    elif hasattr(v,'__dict__'):
                                        set_sub_obj(k,v.__dict__)

                for k,v in attr_dicts:
                    p = self.GetPropertyByName(k)
                    if not p:
                        raise AssertionError("No such property: '%s'"%k)
                    for an,av in v.items():
                        p.SetAttribute(an, av)


            cur_page = False
            is_manager = isinstance(self, PropertyGridManager)

            try:
                set_sub_obj(self.GetGrid().GetRoot(), dict_)
            except:
                import traceback
                traceback.print_exc()

            self.Refresh()
            """)

    # TODO: should these be marked as deprecated? Probably...
    module.addPyCode("""\
        PropertyGridInterface.GetValues = PropertyGridInterface.GetPropertyValues
        PropertyGridInterface.SetValues = PropertyGridInterface.SetPropertyValues
        """)


    c.addPyMethod('_AutoFillMany', '(self,cat,dict_)',
        body="""\
            for k,v in dict_.items():
                self._AutoFillOne(cat,k,v)
            """)

    c.addPyMethod('_AutoFillOne', '(self,cat,k,v)',
        body="""\
            global _type2property
            factory = _type2property.get(v.__class__,None)
            if factory:
                self.AppendIn(cat, factory(k,k,v))
            elif hasattr(v,'__dict__'):
                cat2 = self.AppendIn(cat, PropertyCategory(k))
                self._AutoFillMany(cat2, v.__dict__)
            elif isinstance(v, dict):
                cat2 = self.AppendIn(cat, PropertyCategory(k))
                self._AutoFillMany(cat2, v)
            elif not k.startswith('_'):
                raise AssertionError("member '%s' is of unregistered type/"
                                     "class '%s'"%(k,v.__class__))
            """)

    c.addPyMethod('AutoFill', '(self, obj, parent=None)',
        doc="""\
            "Clears properties and re-fills to match members and values of
            the given object or dictionary obj.
            """,
        body="""\
            self.edited_objects[parent] = obj

            cur_page = False
            is_manager = isinstance(self, PropertyGridManager)

            if not parent:
                if is_manager:
                    page = self.GetCurrentPage()
                    page.Clear()
                    parent = page.GetRoot()
                else:
                    self.Clear()
                    parent = self.GetGrid().GetRoot()
            else:
                it = self.GetIterator(PG_ITERATE_PROPERTIES, parent)
                it.Next()  # Skip the parent
                while not it.AtEnd():
                    p = it.GetProperty()
                    if not p.IsSomeParent(parent):
                        break

                    self.DeleteProperty(p)

                    name = p.GetName()
                    it.Next()

            if not is_manager or page == self.GetCurrentPage():
                self.Freeze()
                cur_page = True

            try:
                self._AutoFillMany(parent,obj.__dict__)
            except:
                import traceback
                traceback.print_exc()

            if cur_page:
                self.Thaw()
            """)


    c.addPyMethod('RegisterEditor', '(self, editor, editorName=None)',
        doc="Register a new editor, either an instance or a class.",
        body="""\
            if not isinstance(editor, PGEditor):
                editor = editor()
            if not editorName:
                editorName = editor.__class__.__name__
            try:
                self._editor_instances.append(editor)
            except:
                self._editor_instances = [editor]
            return PropertyGrid.DoRegisterEditorClass(editor, editorName)
            """
        )


    c.find('GetPropertyClientData').ignore()
    c.addPyMethod('GetPropertyClientData', '(self, p)',
        body="""\
            if isinstance(p, str):
                p = self.GetPropertyByName(p)
            return p.GetClientData()
            """)

    c.find('SetPropertyClientData').ignore()
    c.addPyMethod('SetPropertyClientData', '(self, p, data)',
        body="""\
            if isinstance(p, str):
                p = self.GetPropertyByName(p)
            return p.SetClientData(data)
            """)



    c.addPyMethod('GetPyIterator', '(self, flags=PG_ITERATE_DEFAULT, firstProperty=None)',
        doc="""\
            Returns a pythonic property iterator for a single :ref:`PropertyGrid`
            or page in :ref:`PropertyGridManager`. Arguments are same as for
            :ref:`GetIterator`.

            The following example demonstrates iterating absolutely all items in
            a single grid::

                iterator = propGrid.GetPyIterator(wx.propgrid.PG_ITERATE_ALL)
                for prop in iterator:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Properties`
                  `wx.propgrid.PropertyGridInterface.Items`
            """,
        body="""\
            it = self.GetIterator(flags, firstProperty)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()
            """)


    c.addPyMethod('GetPyVIterator', '(self, flags=PG_ITERATE_DEFAULT)',
        doc="""\
            Similar to :ref:`GetVIterator` but returns a pythonic iterator.
            """,
        body="""\
            it = self.GetVIterator(flags)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()
            """)


    c.addPyMethod('_Properties', '(self)',
        doc="""\
            This attribute is a pythonic iterator over all properties in
            this `PropertyGrid` property container. It will only skip
            categories and private child properties. Usage is simple::

                for prop in propGrid.Properties:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Items`
                  `wx.propgrid.PropertyGridInterface.GetPyIterator`
            """,
        body="""\
            it = self.GetIterator(PG_ITERATE_NORMAL)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()
            """)
    c.addPyProperty('Properties', '_Properties')


    c.addPyMethod('_Items', '(self)',
        doc="""\
            This attribute is a pythonic iterator over all items in this
            `PropertyGrid` property container, excluding only private child
            properties. Usage is simple::

                for prop in propGrid.Items:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Properties`
                  `wx.propgrid.PropertyGridInterface.GetPyVIterator`
            """,
        body="""\
            it = self.GetVIterator(PG_ITERATE_NORMAL | PG_ITERATE_CATEGORIES)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()
            """)
    c.addPyProperty('Items', '_Items')


    def postProcessReST(text):
        # fix some autodoc glitches
        text = text.replace(':ref:`PropertyGridIterator Flags <propertygriditerator flags>`',
                            ':ref:`wx.propgrid.PG_ITERATOR_FLAGS`')
        return text

    c.setReSTPostProcessor(postProcessReST)

    #----------------------------------------------------------

    module.addItem(
        tools.wxArrayPtrWrapperTemplate('wxArrayPGProperty', 'wxPGProperty', module))



    # wxPGPropArg is a typedef for "const wxPGPropArgCls&" so having the
    # wrappers treat it as a normal type can be problematic. ("new cannot be
    # applied to a reference type", etc.) Let's just ignore it and replace it
    # everywhere for the real type.
    module.find('wxPGPropArg').ignore()
    for item in module.allItems():
        if hasattr(item, 'type') and item.type == 'wxPGPropArg':
            item.type = 'const wxPGPropArgCls &'


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

