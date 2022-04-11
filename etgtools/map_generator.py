# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        etgtools/map_generator.py
# Author:      Robin Dunn
#
# Created:     20-May-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
# ---------------------------------------------------------------------------

"""
This generator simply maintains a persistent map of top-level item names and
the module each is in.  This will be used in the Sphinx generator and will
perhaps help simplify other generator tasks as well.
"""


# Phoenix-specific imports
from . import extractors
from . import generators
from .tweaker_tools import removeWxPrefix
from .item_module_map import ItemModuleMap
from sphinxtools.constants import MODULENAME_REPLACE

# ---------------------------------------------------------------------------

class ItemMapGenerator(generators.DocsGeneratorBase):
    def __init__(self):
        super(ItemMapGenerator, self).__init__()

    def generate(self, module):
        assert isinstance(module, extractors.ModuleDef)
        realModuleName = MODULENAME_REPLACE[module.module]

        dispatchMap = {
            extractors.ClassDef : self.generateClass,
            extractors.EnumDef: self.generateEnum,
        }

        imm = ItemModuleMap()
        for item in module.items:
            func = dispatchMap.get(item.__class__, self.generateDefault)
            func(item, imm, realModuleName)

        imm.flush()


    def generateClass(self, item, imm, scope):
        # Map names for classes, nested classes and nested enums
        if item.ignored:
            return
        name = self._getName(item)
        if not name or name.startswith('@'):
            return

        imm[name] = scope

        # are there nested classes?
        for inner in item.innerclasses:
            self.generateClass(inner, imm, '{}{}.'.format(scope, name))

        # Check for nested enums too
        for classItem in item.items:
            if isinstance(classItem, extractors.EnumDef):
                self.generateEnum(
                    classItem, imm, '{}{}.'.format(scope, name), False)


    def generateEnum(self, item, imm, scope, topLevel=True):
        # map names of enum types and enum elements
        if item.ignored:
            return
        name = self._getName(item)
        if name and not name.startswith('@'):
            imm[name] = scope

        # TODO: Investigate if there are cases where nested enum elements
        # should be tracked too.
        if topLevel:
            # Also add an entry for the elements of the enum, as they are also
            # names accessible from the top-level namespace.
            for enum in item:
                self.generateDefault(enum, imm, scope)


    def generateDefault(self, item, imm, scope):
        # this handles all types that don't need special attention
        if item.ignored:
            return
        name = self._getName(item)
        if not name or name.startswith('@'):
            return
        imm[name] = scope


    def _getName(self, item):
        return item.pyName if item.pyName else removeWxPrefix(item.name)

# ---------------------------------------------------------------------------


